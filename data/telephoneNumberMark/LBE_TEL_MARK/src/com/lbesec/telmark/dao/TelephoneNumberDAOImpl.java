package com.lbesec.telmark.dao;

import java.util.HashMap;
import java.util.Map;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

import com.lbesec.telmark.db.DBOpenHelper;

public class TelephoneNumberDAOImpl implements TelephoneNumberDAO {

    private DBOpenHelper helper = null;
    private String table_name = "number_mark";

    public TelephoneNumberDAOImpl(Context context) {
        helper = new DBOpenHelper(context);
    }

    @Override
    public boolean updateNum(ContentValues values, String whereClause, String[] whereArgs) {
        boolean flag = false;
        SQLiteDatabase database = null;
        int count = 0;
        try {
            database = helper.getWritableDatabase();
            count = database.update(table_name, values, whereClause, whereArgs);
            flag = (count > 0 ? true : false);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (database != null) {
                database.close();
            }
        }
        return flag;
    }

    @Override
    public Map<String, String> numInfo(String selection, String[] selectionArgs) {
        Map<String, String> map = new HashMap<String, String>();
        SQLiteDatabase database = null;
        Cursor cursor = null;

        try {
            database = helper.getReadableDatabase();
            cursor = database.query(true, table_name, null, selection, selectionArgs,
                    null, null, null, null);
            int cols_len = cursor.getColumnCount(); // 获取游标个数，即查询所得的结果数目
            while (cursor.moveToNext()) {
                for (int i = 0; i < cols_len; i++) {
                    String name = cursor.getColumnName(i);
                    String value = cursor.getString(cursor.getColumnIndex(name));
                    if (value == null) {
                        value = "";
                    }
                    map.put(name, value);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (database != null) {
                database.close();
            }
        }
        return map;
    }

    @Override
    public Map<String, String> listNumInfo(String selection, String[] selectionArgs) {
        Map<String, String> nums = new HashMap<String, String>();
        SQLiteDatabase database = null;
        Cursor cursor = null;
        try {
            database = helper.getReadableDatabase();
            // cursor = database.query(false, table_name, null, selection,
            // selectionArgs, null, null, null, null);
            String sql = "select id, number from number_mark where is_search = 0 limit 1;";
            cursor = database.rawQuery(sql, selectionArgs);
            int cols_len = cursor.getColumnCount(); // 值为2
            while (cursor.moveToNext()) {
                String k = null;
                String v = null;
                for (int i = 0; i < cols_len; i++) {
                    String name = cursor.getColumnName(i);
                    String value = cursor.getString(cursor.getColumnIndex(name));
                    if (value == null) {
                        value = "";
                    }
                    if (i == 0) {
                        k = value;
                    } else {
                        v = value;
                    }

                }
                if (k != null && v != null) {
                    nums.put(k, v);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (database != null) {
                database.close();
            }
        }
        return nums;
    }

    @Override
    public int count() {
        int result = 0;
        SQLiteDatabase database = null;
        Cursor cursor = null;

        try {
            String sql = "select count(*) from number_mark;";
            database = helper.getReadableDatabase();
            cursor = database.rawQuery(sql, null);
            while (cursor.moveToNext()) {
                result = cursor.getInt(0);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (database != null) {
                database.close();
            }
        }
        return result;
    }

    // @Override
    // public boolean updateNum(Object[] params) {
    // boolean flag = false;
    // SQLiteDatabase database = null;
    // try {
    // String sql = "update number_mark set " +
    // "new_type = ?" +
    // ", new_count = ?" +
    // ", info = ?" +
    // ", is_search = 1 " +
    // "where number = ?";
    // database = helper.getWritableDatabase();
    // database.execSQL(sql, params);
    // flag = true;
    // } catch (Exception e) {
    // e.printStackTrace();
    // } finally {
    // if(database != null) {
    // database.close();
    // }
    // }
    // return flag;
    // }
    //
    // @Override
    // public Map<String, String> numInfo(String[] args) {
    // // TODO Auto-generated method stub
    // return null;
    // }
    //
    // @Override
    // public List<Map<String, String>> listNumInfo(String[] args) {
    // List<Map<String, String>> nums = new ArrayList<Map<String,String>>();
    // SQLiteDatabase database = null;
    // try {
    // String sql = "";
    // database = helper.getReadableDatabase();
    // Cursor cursor = database.rawQuery(sql, args);
    // int colums = cursor.getColumnCount(); // 获得数据库的列的个数
    // while (cursor.moveToNext()) {
    // Map<String, String> map = new HashMap<String, String>();
    //
    // for(int i=0; i<colums; i++) {
    // String name = cursor.getColumnName(i);
    // String value = cursor.getString(i);
    // if(name == null) { // 数据库中有写记录是允许有空值的,所以这边需要做一个处理
    // name = "";
    // }
    // map.put(name, value);
    // }
    //
    // nums.add(map);
    // }
    // } catch (Exception e) {
    // e.printStackTrace();
    // } finally {
    // if(database != null) {
    // database.close();
    // }
    // }
    // return nums;
    // }

}
