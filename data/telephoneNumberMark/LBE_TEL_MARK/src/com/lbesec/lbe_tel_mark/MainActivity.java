package com.lbesec.lbe_tel_mark;

import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Timer;
import java.util.TimerTask;

import android.app.Activity;
import android.content.ContentValues;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

import com.lbesec.main.Main;
import com.lbesec.telmark.dao.TelephoneNumberDAO;
import com.lbesec.telmark.dao.TelephoneNumberDAOImpl;
import com.lbesec.telmark.db.DBOpenHelper;
import com.lbesec.telmark.log.Logger;

public class MainActivity extends Activity {

    private static final String TAG_STRING = "MainActivity";

    private final Logger logger = Logger.getLogger();
    
    private Button btn_create_table;

    private Button btn_start_or_stop;

    private TextView mTextView = null;

    private Timer mTimer = null;

    private TimerTask mTimerTask = null;

    private Handler mHandler = null;

//    private static int count = 0;

    private boolean isStop = true;

    private boolean isPause = false;

    private static int delay = 1000; // 1s

    private static int period = 1000; // 1s

    private static final int UPDATE_TEXTVIEW = 0;

    private static String db_count = null;

    private static String db_select_id = null;

    private static String db_number = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initComponent();

        btn_create_table.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                DBOpenHelper helper = new DBOpenHelper(MainActivity.this);
                helper.getWritableDatabase();
                Log.i(TAG_STRING, "---- create table --->");
            }
        });

        btn_start_or_stop.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                if (isStop) {
                    Log.i(TAG_STRING, "Start");
                } else {
                    Log.i(TAG_STRING, "Stop");
                }

                isStop = !isStop;

                if (!isStop) {
                    startTimer();
                } else {
                    stopTimer();
                }

                if (isStop) {
                    btn_start_or_stop.setText(R.string.start);
                } else {
                    btn_start_or_stop.setText(R.string.stop);
                }
            }
        });

        mHandler = new Handler() {

            @Override
            public void handleMessage(Message msg) {
                switch (msg.what) {
                    case UPDATE_TEXTVIEW:
                        updateTextView();
                        break;
                    default:
                        break;
                }
            }
        };
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    public void initComponent() {
        btn_create_table = (Button) findViewById(R.id.btn_create_table);
        btn_start_or_stop = (Button) findViewById(R.id.btn_start_stop);
        mTextView = (TextView) findViewById(R.id.mytextview);
        
        db_count = String.valueOf(count());
    }

    private void updateTextView() {
        mTextView.setText("DB_COUNT:" + db_count + "\n SELECT_ID: " + db_select_id + "\n NUMBER: " + db_number);
    }

    private void startTimer() {
        if (mTimer == null) {
            mTimer = new Timer();
        }

        if (mTimerTask == null) {
            mTimerTask = new TimerTask() {
                @Override
                public void run() {
//                    Log.i(TAG_STRING, "count: " + String.valueOf(count));

//                    logger.debug("count: " + String.valueOf(count));
//                    db_select_id = numInfo(" number = ? ", new String[] {"0010086" }).get("id");
                    Map<String, String> numInfos = listNumInfo();
                    if(!numInfos.isEmpty()) {
                        Iterator<Entry<String, String>> infos = numInfos.entrySet().iterator();
                        while(infos.hasNext()) {
                            Map.Entry<String, String> entry = (Entry<String, String>) infos.next();
                            db_select_id = entry.getKey();
                            db_number = entry.getValue();
                            String[] crawelInfo = new Main().foundNumber(db_number);
                            boolean isupdate = updateNum(crawelInfo, db_select_id);
//                            boolean isupdate = updateNum(new String[] {"中国移动客服", null, null}, db_select_id);
                            if(isupdate) {
                                Log.i(TAG_STRING, String.format("---- update id(%s) number(%s) info success. --->", db_select_id, db_number));
                            }
                        }
                    }
                    
                    sendMessage(UPDATE_TEXTVIEW);
                    do {
                        try {
                            Log.i(TAG_STRING, "sleep(1000)...");
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                        }
                    } while (isPause);

//                    count++;
                }
            };
        }

        if (mTimer != null && mTimerTask != null)
            mTimer.schedule(mTimerTask, delay, period);

    }

    private void stopTimer() {

        if (mTimer != null) {
            mTimer.cancel();
            mTimer = null;
        }

        if (mTimerTask != null) {
            mTimerTask.cancel();
            mTimerTask = null;
        }

//        count = 0;
//        db_count = null;
        db_select_id = null;
        db_number = null;

    }

    public void sendMessage(int id) {
        if (mHandler != null) {
            Message message = Message.obtain(mHandler, id);
            mHandler.sendMessage(message);
        }
    }

    public boolean updateNum(String[] infos, String id) {
        boolean flag = false;
        if (infos.length != 3) {
            return flag;
        }
        if(infos[0] == null && infos[1] == null && infos[2] == null) {
            Log.i(TAG_STRING, String.format("ID(%s) no found", id));
        }
        TelephoneNumberDAO dao = new TelephoneNumberDAOImpl(MainActivity.this);
        ContentValues values = new ContentValues();
        values.put("info", infos[0]);
        values.put("new_type", infos[1]);
        values.put("new_count", infos[2]);
        values.put("is_search", 1);
        flag = dao.updateNum(values, " id = ? ", new String[] { id });

        return flag;
    }

    public Map<String, String> numInfo(String selection, String[] selectionArgs) {
        TelephoneNumberDAO dao = new TelephoneNumberDAOImpl(MainActivity.this);
        // Map<String, String> map = dao.numInfo(" number = ? ", new String[] {
        // "18126110496" });
        Map<String, String> map = dao.numInfo(selection, selectionArgs);
        return map;
    }

    public Map<String, String> listNumInfo() {
        TelephoneNumberDAO dao = new TelephoneNumberDAOImpl(MainActivity.this);
        Map<String, String> list_number_info = dao.listNumInfo(null, null);
        return list_number_info;
    }

    public int count() {
        TelephoneNumberDAO dao = new TelephoneNumberDAOImpl(MainActivity.this);
        int result = dao.count();
        Log.i(TAG_STRING, "execute");
        return result;
    }
}
