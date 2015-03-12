package com.lbesec.tel.mark.crawel;

//import org.apache.commons.logging.Log;
//import org.apache.commons.logging.LogFactory;

public abstract class Crawel {

    // private static Log log = LogFactory.getLog(Crawel.class);

    /**
     * 获取标记号码信息
     * 
     * @param num
     * @return
     */
    public abstract String[] getNumberInfo(String num);

    public static void print(Object msg) {
        System.out.println(msg);
        // log.equals(msg);
    }
}
