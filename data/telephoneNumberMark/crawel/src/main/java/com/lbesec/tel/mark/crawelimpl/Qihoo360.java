package com.lbesec.tel.mark.crawelimpl;

import static com.gistlabs.mechanize.document.html.query.HtmlQueryBuilder.*;

import com.gistlabs.mechanize.MechanizeAgent;
import com.gistlabs.mechanize.document.Document;
import com.gistlabs.mechanize.document.html.HtmlDocument;
import com.gistlabs.mechanize.document.html.HtmlElement;
import com.gistlabs.mechanize.document.html.form.Form;
import com.lbesec.common.Constant;
import com.lbesec.tel.mark.crawel.Crawel;

public class Qihoo360 extends Crawel {

    private static String uri = "http://m.so.com/";

    public String[] getNumberInfo(String num) {
        String[] result = new String[3];
        MechanizeAgent agent = new Constant().agent();
        Document page = agent.get(uri);
        agent.idle(200);
        try {
            Form search = page.forms().get(0);
            search.get("q").set(num);
            agent.idle(250);

            HtmlDocument response = (HtmlDocument) search.submit();
            agent.idle(250);

            HtmlElement mark = response.htmlElements().get(byClass("mh-tel-mark"));
            HtmlElement desc = response.htmlElements().get(byClass("mh-tel-desc"));

            if (mark != null && desc != null) {
                String info = mark.getText();
                String count = desc.get(byTag("b")).getText();

                result[0] = info;
//                result[1] = info;
                result[2] = count;

                // print(info);
                // print(type);
                // print(count);
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
         * 骚扰电话 骚扰电话 5861
         */

        String num = "01053579320";
        Qihoo360 qihoo360 = new Qihoo360();
        String[] infos = qihoo360.getNumberInfo(num);
        for(String info: infos) {
            print(info);
        }

    }

    public static void main(String[] args) {
        test();
    }
}
