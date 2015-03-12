package com.lbesec.tel.mark.crawelimpl;

import com.gistlabs.mechanize.MechanizeAgent;
import com.gistlabs.mechanize.document.Document;
import com.lbesec.common.Constant;
import com.lbesec.tel.mark.crawel.Crawel;

import org.json.JSONObject;

public class Sogou extends Crawel {

    private static String uri = "http://data.haoma.sogou.com/vrapi/query_number.php?number=%s&type=json&callback=show";

    public String[] getNumberInfo(String num) {
        String[] result = new String[3];
        String urlString = String.format(uri, num);
        // print(urlString);
        MechanizeAgent agent = new Constant().agent();
        Document page = agent.get(urlString);
        agent.idle(2000);

        try {
            String text = page.getRoot().getValue();
            // String text =
            // "show({\"NumInfo\":\"\u53f7\u7801\u901a\u7528\u6237\u6570\u636e\uff1a\u63a8\u9500\",\"errorCode\":0,\"Amount\":\"96\"})";
            // String text =
            // "show({\"description\":\"\u53f7\u7801\u4e0d\u7b26\u5408\u89c4\u8303\",\"errorCode\":11014})";
            if (text.length() > 0) {
                text = text.replace("show(", "").replace(")", "");
                JSONObject json = new JSONObject(text);

                if (json.isNull("NumInfo") || json.isNull("Amount")) {
                    print(json);
                } else {
                    String info = json.get("NumInfo").toString();
                    String count = json.get("Amount").toString();
                    if (info.contains("：")) {
                        info = info.split("：")[1];
                    }
                    result[0] = info;
                    // result[1] = info;
                    result[2] = count;

                    // print(info);
                    // print(count);
                    // print("==========");
                }

            } else {
                print("No Found.");
            }
        } catch (Exception e) {
            print(e);
        }

        return result;
    }

    public static void test() {
        // String num = "世界杯";
        /*
         * 推销 105 ========== 
         * 推销 92 ========== 
         * 推销 96 ========== 
         * 智联招聘 64========== 
         * {"description":"号码不符合规范","errorCode":11014}
         */

        // String num = "01050839013";
        String[] nums = { "01050839061", "01050839043", "01050839013", "01050833000",
                "0104008260350" };
        Sogou sogou = new Sogou();
        for (String num : nums) {
            String[] infos = sogou.getNumberInfo(num);
            for (String info : infos) {
                print(info);
            }
        }

    }

    public static void main(String[] args) {
        test();
    }
}
