package com.lbesec.main;

import com.lbesec.tel.mark.crawel.Crawel;
import com.lbesec.tel.mark.crawelimpl.Baidu;
import com.lbesec.tel.mark.crawelimpl.Qihoo360;
import com.lbesec.tel.mark.crawelimpl.Sogou;
import com.lbesec.util.Utils;

public class Main {

    /**
     * 查找号码标记入口， 1.首先使用搜狗号码通API
     * 2.如果没数据，查找百度 
     * 3.如果没数据，查找360
     * 
     * @param num
     * @return 返回['号码标记信息', '类型', '标记人数']
     */
    public String[] foundNumber(String num) {
        String[] result = new String[3];
        Crawel crawel = null;

        num = Utils.filter(num);
        if (num != null && num.length() > 0) {
            crawel = new Sogou();
            result = crawel.getNumberInfo(num);

            if (result.length > 0 && result[0] == null) {
                crawel = new Baidu();
                result = crawel.getNumberInfo(num);
            }

            if (result.length > 0 && result[0] == null) {
                crawel = new Qihoo360();
                result = crawel.getNumberInfo(num);
            }
        }
        return result;
    }

    
    // * 推销 推销 499 ========== "北京 <18301411946>"
    // * null null null ========== "ABSENT NUMBER"
    // * 优购物订购热线 优购物订购热线 0 ========== "400 707 5678"
    // * {"NumInfo":"该号码暂无标记","errorCode":0} No Found. No Found. null null null ========== "188-2529-1808"
    // * 韵达快递 韵达快递 0 ========== "1790118767719157"
    // * 推销 推销 98 ========== "1252002066693855"
    // * 中国移动客服 中国移动客服 0 ========== "0010086"
    // * 天天快递 天天快递 0 ========== "13201037777"
    // * 诈骗 诈骗 78 ========== "+00861085953400"
    public void test() {
        String[] nums = { "北京 <18301411946>", "ABSENT NUMBER", "400 707 5678",
                "188-2529-1808", "1790118767719157", "1252002066693855", "0010086",
                "13201037777", "+00861085953400" };
        for (String num : nums) {
            String[] infos = foundNumber(num);
            for (String info : infos) {
                System.out.println(info);
            }
            System.out.println("==========");
        }
    }

    public static void main(String[] args) {
        Main main = new Main();
        main.test();
    }

}
