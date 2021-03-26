#!/usr/bin/env python

from pg import DB
import os
import shutil
import re
from time import time, sleep
import subprocess


class TPCDS:

    STORAGE = [
        ("small_storage", "appendonly=true, orientation=column"),
        ("medium_storage", "appendonly=true, orientation=column, compresstype=zstd"),
        ("large_storage", "appendonly=true, orientation=column, compresstype=zstd"),
        ("e9_medium_storage", "appendonly=true, compresstype=zstd"),
        ("e9_large_storage", "appendonly=true, orientation=column, compresstype=zstd")
    ]

    RAW_DATA_PATH = "/data/generated_source_data/data"

    def __init__(self, info_dir, dbname, port, host, data_path):
        self.info_dir = info_dir
        self.db = DB(dbname=dbname, port=port, host=host)
        self.dist_info = self.parse_dist_info()
        self.data_path = data_path

    def create_schema(self):
        sqls = [
            "DROP SCHEMA IF EXISTS tpcds CASCADE;",
            "DROP SCHEMA IF EXISTS ext_tpcds CASCADE;",
            "CREATE SCHEMA tpcds;",
            "CREATE SCHEMA ext_tpcds;"
        ]
        for sql in sqls:
            self.db.query(sql)

    def create_table(self):
        ddl_top_path = os.path.join(self.info_dir, "ddl")
        print("creating norm tables...")
        for fn in os.listdir(ddl_top_path):
            if not fn.endswith(".sql"): continue
            if fn == "000.e9.tpcds.sql": continue
            if "ext_" in fn: continue
            self.create_normal_table(os.path.join(ddl_top_path, fn))
        print("norm tables created.")

        print("creating ext tables...")        
        for fn in os.listdir(ddl_top_path):
            if not fn.endswith(".sql"): continue
            if fn == "000.e9.tpcds.sql": continue
            if "ext_" not in fn: continue
            self.create_ext_table(os.path.join(ddl_top_path, fn))
        print("ext tables created.")

    def create_normal_table(self, ddlpath):
        assert("ext_" not in ddlpath)
        with open(ddlpath) as f:
            sql = f.read().lower()
        tabname = self.get_tabname_from_path(ddlpath)
        sql = self.patch_dist_info(sql, tabname)
        sql = self.patch_storage_info(sql)
        self.db.query(sql)

    def create_ext_table(self, ddlpath):
        assert("ext_" in ddlpath)
        with open(ddlpath) as f:
            sql = f.read().lower()
        tabname = self.get_tabname_from_path(ddlpath)
        sql = self.patch_gpfdist_local(sql, tabname)
        self.db.query(sql)

    def patch_dist_info(self, sql, tabname):
        distkeys = self.dist_info[tabname]
        sql = sql.replace(":distributed_by",
                          "distributed by (%s)" % distkeys)
        return sql

    def patch_storage_info(self, sql):
        for storage_type, storage_option in self.STORAGE:
            replace_key = ":" + storage_type
            sql = sql.replace(replace_key, storage_option)
        return sql

    def patch_gpfdist_local(self, sql, tabname):
        url = "'gpfdist://mdw:2223/%s*.dat'" % tabname
        sql = sql.replace(":location", url)
        return sql
    
    def get_tabname_from_path(self, path):
        filename = os.path.basename(path)
        return filename.split(".")[-2]

    def parse_dist_info(self):
        dist_info = {}
        with open(os.path.join(self.info_dir, "ddl", "distribution.txt")) as f:
            for line in f:
                _, tabname, distkeys = line.strip().split("|")
                dist_info[tabname] = distkeys
        return dist_info

    def start_gpfdist(self, port, logfile):
        cmd = ["gpfdist",
               "-p", str(port),
               "-l", logfile]
        proc = subprocess.Popen(cmd)
        sleep(3)
        return proc

    def load_all_tables(self):
        ddl_top_path = os.path.join(self.info_dir, "ddl")
        start_time = time()
        print("load tables...")
        print("===================================")
        for fn in os.listdir(ddl_top_path):
            if not fn.endswith(".sql"): continue
            if fn == "000.e9.tpcds.sql": continue
            if "ext_" in fn: continue
            self.load_table(os.path.join(ddl_top_path, fn))
        end_time = time()
        cost = end_time - start_time
        print("all tables finished in %s seconds" % cost)

    def load_table(self, ddlpath):
        tabname = self.get_tabname_from_path(ddlpath)
        tab_data_path = self.get_tab_data_path(tabname)
        os.chdir(tab_data_path)
        proc = self.start_gpfdist("2223", "/data/gpfdist.log")
        sql = ("insert into tpcds.%s "
               "select * from ext_tpcds.%s") % (tabname, tabname)
        start_time = time()
        self.db.query(sql)
        end_time = time()
        proc.terminate()
        proc.wait()
        cost = end_time - start_time
        print("load %s cost time %s seconds" % (tabname, cost))
        print("===================================")

    def get_tab_data_path(self, tabname):
        return os.path.join(self.data_path, tabname)

    def move_all_tables(self):
        ddl_top_path = os.path.join(self.info_dir, "ddl")
        for fn in os.listdir(ddl_top_path):
            if not fn.endswith(".sql"): continue
            if fn == "000.e9.tpcds.sql": continue
            if "ext_" in fn: continue
            self.move_table(os.path.join(ddl_top_path, fn))

    def move_table(self, ddlpath):
        tabname = self.get_tabname_from_path(ddlpath)
        fns = self.findall_tab_data(tabname)
        newplace = os.path.join(self.data_path, tabname)
        os.makedirs(newplace, exist_ok=True)
        for fn in fns:
            shutil.move(fn, newplace)
        print("moving %s (%d dat files)" % (tabname, len(fns)))

    def findall_tab_data(self, tabname):
        data_fns = []
        pt_regstr = tabname + r"_\d+_\d+.dat"
        pt = re.compile(pt_regstr)
        for fn in os.listdir(self.RAW_DATA_PATH):
            if pt.search(fn):
                data_fns.append(os.path.join(self.RAW_DATA_PATH, fn))
        return data_fns

    def close_db(self):
        self.db.close()


if __name__ == "__main__":
    tpcds = TPCDS("/home/gpadmin/benchmarks/tpcds/gp-performance-testing/tpc-ds",
                  "tpcds",
                  5432,
                  "mdw",
                  "/data/tpcds-data")
    tpcds.create_schema()
    tpcds.create_table()
    tpcds.load_all_tables()
    tpcds.close_db()
