
DB_VERSION = 3

class DbSchema:
    def __init__(self):
        self.tables = {}
        self.indexes = {}
        self._populate_tables()
        self.views = {}

    def _populate_tables(self):
        # blocks table
        blocks = """
            CREATE TABLE IF NOT EXISTS blocks (
                num integer PRIMARY KEY,
                hash char(40) NOT NULL,
                prev char(40),
                timestamp timestamp NOT NULL
            );"""
        self.tables['blocks'] = blocks
        
        # custom_json_ops table
        custom_json_ops = """
            CREATE TABLE IF NOT EXISTS custom_json_ops (
                id serial PRIMARY KEY,
                block_num integer NOT NULL REFERENCES blocks (num),
                transaction_id char(40) NOT NULL,
                req_auths varchar(16)[],
                req_posting_auths varchar(16)[],
                op_id varchar(128) NOT NULL,
                op_json json NOT NULL
            );"""
        self.tables['custom_json_ops'] = custom_json_ops

        # podping table
        # [TODO] create conditionally, this table should only be created 
        # if configuration files identify inclusion of podping tabels
        podping = """
            CREATE TABLE IF NOT EXISTS public.podping_url (
                id serial,
                custom_json_ops_id integer,
                url varchar NOT NULL,
                reason varchar(255),
                domain varchar,
                version varchar(16),
                PRIMARY KEY (id),
                CONSTRAINT custom_json_ops_id_fkey FOREIGN KEY (custom_json_ops_id)
                    REFERENCES public.custom_json_ops (id) MATCH SIMPLE
            );"""

        # The for storage and performance each of the columns 
        # 'url', 'reason', 'domain', and 'version' could 
        # be normalized as separate 'one to many' and changed to _id integer values for separate tables ...
        
        self.tables['podping'] = podping

        global_props = """
            CREATE TABLE IF NOT EXISTS global_props (
                db_version smallint
            );"""
        self.tables['global_props'] = global_props

    def _create_indexes(self):
        blocks_ix_num = """
            CREATE INDEX blocks_ix_num
            ON blocks (num)
        ;"""
        self.indexes['blocks_ix_num'] = blocks_ix_num

        custom_json_ops_ix_block_num = """
            CREATE INDEX custom_json_ops_ix_block_num
            ON custom_json_ops (block_num)
        ;"""
        self.indexes['custom_json_ops_ix_block_num'] = custom_json_ops_ix_block_num
        
        podping_url_ix = """
            CREATE INDEX podping_url_ix
            ON podping (url)
        ;"""
        self.indexes['podping_url_ix'] = podping_url_ix
        
