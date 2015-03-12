package com.lbesec.telmark.db;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

public class DBOpenHelper extends SQLiteOpenHelper {

    private static String name = "lbe_tel_mark.db";
    
    private static int version = 1;
    
    public DBOpenHelper(Context context) {
        super(context, name, null, version);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        String sql = "CREATE TABLE IF NOT EXISTS number_mark (" +
                "id INTEGER PRIMARY KEY," +
                "number varchar(100) DEFAULT NULL," +
                "type varchar(100) DEFAULT NULL," +
                "count int(11) DEFAULT NULL," +
                "new_type varchar(100) DEFAULT NULL," +
                "new_count int(11) DEFAULT NULL," +
                "info varchar(500) DEFAULT NULL," +
                "created_date datetime DEFAULT NULL," +
                "is_search tinyint(4) NOT NULL DEFAULT '0'" +
                ")";
        db.execSQL(sql);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // TODO Auto-generated method stub

    }

}
