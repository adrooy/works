package com.dch.helloandroid;

import java.io.BufferedReader;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.security.MessageDigest;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;

import com.lib.common.tool.PPIncrementalUpdate;
import com.taobao.bspatch.BSPatch;

import android.content.Intent;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Toast;

public class MainActivity extends ActionBarActivity {

//    static {
//        try {//防止出现不支持的CPU，如MIPS等，而导致出现Error
//            System.loadLibrary("IncrementalUpdate");
//            System.loadLibrary("ppapkpatchso");
//        } catch (Throwable e) {
//            System.out.println(e);
//        }
//    }

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

        Button btnSecond=(Button)findViewById(R.id.second);
        btnSecond.setOnClickListener(new OnClickListener() {
            @Override  
            public void onClick(View v) {  
                
            	//BSPatch.test();

                String storagePath = Environment.getExternalStorageDirectory().getAbsolutePath();
//                Toast.makeText(getApplicationContext(), storagePath,
//                        Toast.LENGTH_SHORT).show();

//                writeFileSdcardFile(storagePath + "/test/test", "test");

//                String old = storagePath + "/test/com.sohu.inputmethod.sogou-2.apk";
//                String patch = storagePath + "/test/sougou.aup";
//                String newFile = storagePath + "/test/sougou.apk";

                String old = storagePath + "/test/com.youku.phone-1.apk";
                String patch = storagePath + "/test/youku.aup";
                String newFile = storagePath + "/test/youku.apk";

                long start = Calendar.getInstance().getTimeInMillis();

                int ret = PPIncrementalUpdate.merge(old, patch, newFile);

                long end = Calendar.getInstance().getTimeInMillis();
                long useTime = end-start;

                Toast.makeText(getApplicationContext(), "result: " +  ret + "use time:" + useTime,
                        Toast.LENGTH_SHORT).show();



            	//startActivity(new Intent(MainActivity.this,SecondActivity.class));  
                //finish();//�رյ�ǰActivity  
            }
        });
  
	}


    private void writeFileSdcardFile(String fileName, String writeStr){
        try {

            FileOutputStream fout = new FileOutputStream(fileName);
            byte[] bytes = writeStr.getBytes();

            fout.write(bytes);
            fout.close();

        } catch (Exception e) {
            Toast.makeText(getApplicationContext(), e.getMessage(),
                    Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }
    }

    @Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
	
	



}
