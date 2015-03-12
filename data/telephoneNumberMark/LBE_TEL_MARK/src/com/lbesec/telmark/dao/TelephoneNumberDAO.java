package com.lbesec.telmark.dao;

import java.util.Map;

import android.content.ContentValues;

public interface TelephoneNumberDAO {
    
    // boolean updateNum(Object[] params);
    //
    // Map<String, String> numInfo(String[] args);
    //
    // List<Map<String, String>> listNumInfo(String[] args);
    
    boolean updateNum(ContentValues values, String whereClause, String[] whereArgs);

    /**
     * 根据号码查找号码信息
     * @param selection
     * @param selectionArgs
     * @return
     */
    Map<String, String> numInfo(String selection, String[] selectionArgs);

    /**
     * 显示号码信息，返回一个map。以id为key,number为value
     * @param selection
     * @param selectionArgs
     * @return
     */
    Map<String, String> listNumInfo(String selection, String[] selectionArgs);

    /**
     * 查询数据库中总数
     * @return
     */
    int count();
}
