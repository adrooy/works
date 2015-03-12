package com.lbesec.tel.mark.crawelimpl;

import static com.gistlabs.mechanize.document.html.query.HtmlQueryBuilder.*;

import com.gistlabs.mechanize.MechanizeAgent;
import com.gistlabs.mechanize.document.Document;
import com.gistlabs.mechanize.document.html.HtmlDocument;
import com.gistlabs.mechanize.document.html.HtmlElement;
import com.gistlabs.mechanize.document.html.form.Form;
import com.lbesec.common.Constant;
import com.lbesec.tel.mark.crawel.Crawel;
import com.lbesec.util.Utils;

public class Baidu extends Crawel {

    private static String uri = "http://m.baidu.com/";

    public String[] getNumberInfo(String num) {
        String[] result = new String[3];
        MechanizeAgent agent = new Constant().agent();
        Document page = agent.get(uri);
        agent.idle(200);

        try {
            Form search = page.forms().get(0);
            search.get("word").set(num);
            agent.idle(250);

            HtmlDocument response = (HtmlDocument) search.submit();
            agent.idle(250);

            HtmlElement top = response.htmlElements().get(byClass("wa_liarphone2_top"));
            HtmlElement text = response.htmlElements()
                    .get(byClass("wa_liarphone2_text"));

            if (top != null && text != null) {
                String info = top.get(byTag("span")).getText();
                String type = text.get(byTag("strong")).getText();
                String count = Utils.getNumber(text.getText());
                result[0] = info;
                result[1] = type;
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
//         String num = "baidu yun";
        /*
         * 疑似推销 广告推销 451
         */

        String num = "01053579320";
        Baidu baidu = new Baidu();
        String[] infos = baidu.getNumberInfo(num);
        for(String info: infos) {
            print(info);
        }

    }

    public static void main(String[] args) {
        test();
    }
}
