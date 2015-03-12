package com.lbesec.tel.mark.crawelimpl;

import static com.gistlabs.mechanize.document.html.query.HtmlQueryBuilder.*;

import com.gistlabs.mechanize.MechanizeAgent;
import com.gistlabs.mechanize.document.Document;
import com.gistlabs.mechanize.document.html.HtmlDocument;
import com.gistlabs.mechanize.document.html.HtmlElement;
import com.gistlabs.mechanize.document.html.form.Form;
import com.gistlabs.mechanize.document.html.form.SubmitButton;
import com.gistlabs.mechanize.document.node.Node;
import com.lbesec.common.Constant;
import com.lbesec.tel.mark.crawel.Crawel;

public class Soso extends Crawel {

    private static String uri = "http://wap.soso.com/?g_f=2405";

    public String[] getNumberInfo(String num) {
        String[] result = new String[3];
        MechanizeAgent agent = new Constant().agent();
        Document page = agent.get(uri);
        agent.idle(200);
        try {
            Form search = page.forms().get(0);
            search.get("key").set(num);
            agent.idle(250);

            Node btnNode = page.getRoot();
            SubmitButton btnButton = new SubmitButton(search,
                    btnNode.get(byClass("search_btn")));
            HtmlDocument response = null;
            if (btnButton.getValue() == null) {
                response = (HtmlDocument) search.submit();
            } else {
                response = (HtmlDocument) search.submit(btnButton);
            }

            agent.idle(250);

            // print(response.htmlElements().getRoot().getHtml());
            HtmlElement mark = response.htmlElements().get(byClass("txt-box"));

            if (mark != null) {
                String info = mark.get(byTag("strong")).getText();

                // print(info);
                result[0] = info;
//                result[1] = info;
                result[2] = null;
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
         * 推销 推销 8180
         */

        String num = "4001163166";
        Soso soso = new Soso();
        String[] infos = soso.getNumberInfo(num);
        for(String info: infos) {
            print(info);
        }
        

    }

    public static void main(String[] args) {
        test();
    }
}
