package com.lbesec.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Utils {

    /**
     * 过滤电话号码,分析后号码长度在[5, 13]之间，为正常电话，否则返回null
     * @param num
     * @return
     */
    public static String filter(String num) {

        String[] filter_tag = { "*", "+0086", "0086", "+00", "+86", "+", "17901",
                "17909", "17951", "17911", "12520", "00" };

        num = getNumber(num);
        if(num.length() > 4) {
            for (String tag : filter_tag) {
                if (num.startsWith(tag)) {
                    num = num.replaceFirst(tag, "");
                    break;
                }
            }
        }
        if(num.length() < 5 || num.length() > 13){
            num = null;
        }

        return num;
    }

    /**
     * 获取字符串中数字
     * 
     * @param info
     * @return
     */
    public static String getNumber(String info) {
        String regEx = "[^0-9]";
        Pattern p = Pattern.compile(regEx);
        Matcher m = p.matcher(info);
        return m.replaceAll("").trim();
    }

    public static void test() {
        String[] nums = { "北京 <18301411946>", "ABSENT NUMBER", "400 707 5678",
                "188-2529-1808", "1790118767719157", "1252002066693855", "0010086",
                "13201037777", "+00861085953400", "*p7777*777**77*7" };
        for(String num: nums) {
            System.out.println(filter(num));
        }
    }

    public static void main(String[] args) {
        test();
    }

}
