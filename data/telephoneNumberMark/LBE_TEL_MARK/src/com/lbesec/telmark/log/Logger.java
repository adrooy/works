package com.lbesec.telmark.log;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Environment;
import android.util.Log;

import com.lbesec.lbe_tel_mark.BuildConfig;

public class Logger {
    /**
     * log TAG
     */
    private static String TAG = "Logger";
    private static final String ROOT = Environment.getExternalStorageDirectory()
            .getAbsolutePath() + "/";
    private static String FILE_NAME = "logger.log";

    private static String logFile = ROOT + FILE_NAME;

    /**
     * debug or not
     */
    private static boolean debug = BuildConfig.DEBUG;

    private static boolean write2Sdcard = true;

    private static Logger instance = new Logger();

    private Logger() {

    }

    public static Logger getLogger() {
        System.out.println(ROOT);
        return instance;
    }

    public static Logger getLogger(Context context, String fileName) {
        TAG = context.getPackageName();
        FILE_NAME = fileName;
        return instance;
    }

    /**
     * 获取函数名称
     */
    private String getFunctionName() {
        StackTraceElement[] sts = Thread.currentThread().getStackTrace();

        if (sts == null) {
            return null;
        }

        for (StackTraceElement st : sts) {
            if (st.isNativeMethod()) {
                continue;
            }

            if (st.getClassName().equals(Thread.class.getName())) {
                continue;
            }

            if (st.getClassName().equals(this.getClass().getName())) {
                continue;
            }

            return "[" + Thread.currentThread().getName() + "("
                    + Thread.currentThread().getId() + "): " + st.getFileName() + ":"
                    + st.getLineNumber() + "]";
        }

        return null;
    }

    private String createMessage(String msg) {
        String functionName = getFunctionName();
        String message = (functionName == null ? msg : (functionName + " - " + msg));
        return message;
    }

    /**
     * log.i
     */
    public void info(String msg) {
        String message = createMessage(msg);
        if (debug) {
            Log.i(TAG, message);
        }
        if (write2Sdcard) {
            instance.writeLog(message);
        }
    }

    public static void i(String msg) {
        instance.info(msg);
    }

    public static void i(Exception e) {
        instance.info(e != null ? e.toString() : "null");
    }

    /**
     * log.v
     */
    public void verbose(String msg) {
        String message = createMessage(msg);
        if (debug) {
            Log.v(TAG, message);
        }
        if (write2Sdcard) {
            instance.writeLog(message);
        }
    }

    public void v(String msg) {
        if (debug) {
            instance.verbose(msg);
        }
        if (write2Sdcard) {
            instance.writeLog(msg);
        }
    }

    public void v(Exception e) {
        if (debug) {
            instance.verbose(e != null ? e.toString() : "null");
        }
        if (write2Sdcard) {
            instance.writeLog(e.toString());
        }
    }

    /**
     * log.d
     */
    public void debug(String msg) {
        if (debug) {
            String message = createMessage(msg);
            Log.d(TAG, message);
        }
        if (write2Sdcard) {
            instance.writeLog(msg);
        }
    }

    /**
     * log.e
     */
    public void error(String msg) {
        String message = createMessage(msg);
        if (debug) {
            Log.e(TAG, message);
        }
        if (write2Sdcard) {
            instance.writeLog(message);
        }
    }

    /**
     * log.error
     */
    public void error(Exception e) {
        StringBuffer sb = new StringBuffer();
        String name = getFunctionName();
        StackTraceElement[] sts = e.getStackTrace();

        if (name != null) {
            sb.append(name + " - " + e + "\r\n");
        } else {
            sb.append(e + "\r\n");
        }
        if (sts != null && sts.length > 0) {
            for (StackTraceElement st : sts) {
                if (st != null) {
                    sb.append("[ " + st.getFileName() + ":" + st.getLineNumber()
                            + " ]\r\n");
                }
            }
        }
        if (debug) {
            Log.e(TAG, sb.toString());
        }
        if (write2Sdcard) {
            instance.writeLog(sb.toString());
        }
    }

    /**
     * log.warn
     */
    public void warn(String msg) {
        String message = createMessage(msg);
        if (debug) {
            Log.w(TAG, message);
        }
        if (write2Sdcard) {
            instance.writeLog(message);
        }
    }

    public static void d(String msg) {
        instance.debug(msg);

    }

    public static void d(Exception e) {
        instance.debug(e != null ? e.toString() : "null");
    }

    /**
     * log.e
     * 
     * @description
     * @param msg
     *            hylin 2012-9-20下午2:05:37
     */
    public static void e(String msg) {
        instance.error(msg);
    }

    public static void e(Exception e) {
        instance.error(e);
    }

    /**
     * log.w
     */
    public static void w(String msg) {
        instance.warn(msg);
    }

    public static void w(Exception e) {
        instance.warn(e != null ? e.toString() : "null");
    }

    public static void resetLogFile() {
        File file = new File(logFile);
        file.delete();
        try {
            file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @SuppressLint("SimpleDateFormat")
    private void writeLog(String content) {
        try {
            File file = new File(logFile);
            if (!file.exists()) {
                file.createNewFile();
            }
            // DateFormat formate = SimpleDateFormat.getDateTimeInstance();
            SimpleDateFormat formate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            FileWriter write = new FileWriter(file, true);
            write.write(formate.format(new Date()) + "   " + content + "\n");
            write.flush();
            write.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}