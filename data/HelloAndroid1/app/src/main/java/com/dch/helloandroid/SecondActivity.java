package com.dch.helloandroid;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.security.MessageDigest;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;

import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.app.ListActivity;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.DisplayMetrics;
import android.view.Display;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;
import android.os.Build;

public class SecondActivity extends ListActivity  {

	private Map<String,JSONObject> appMap = new HashMap<String, JSONObject>();
	private String[] COUNTRIES=new String[]{};  
	private ArrayAdapter<String> arrAdapter;
	
		private Handler handler =new Handler(){
		@Override
		//������Ϣ���ͳ�����ʱ���ִ��Handler���������
		public void handleMessage(Message msg){
			super.handleMessage(msg);
			COUNTRIES = (String[]) appMap.keySet().toArray(new String[0]);
			
			arrAdapter = new ArrayAdapter<String>(SecondActivity.this,android.R.layout.simple_list_item_1,COUNTRIES);
			setListAdapter(arrAdapter);
			}
		};
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_second);

		arrAdapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,COUNTRIES);
		setListAdapter(arrAdapter);
		
		new Thread(){
    		@Override
    		public void run(){
    			try {
					getUpdate();
				} catch (MalformedURLException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
    		handler.sendEmptyMessage(0);
    		}
    	}.start();
		
		
        Button btnExit=(Button)findViewById(R.id.exit);
        btnExit.setOnClickListener(new OnClickListener() {
            @Override  
            public void onClick(View v) {  
                finish();
            }  
        });  
	}

	@Override  
	protected void onListItemClick(ListView l, View v, int position, long id) {  
		String showInfo = "size \t" + appMap.get(COUNTRIES[position]).getString("size")
				+ "\npackageName \t" + appMap.get(COUNTRIES[position]).getString("packageName")
				+ "\nversionName \t" + appMap.get(COUNTRIES[position]).getString("versionName")
				+ "\nversionCode \t" + appMap.get(COUNTRIES[position]).getString("versionCode")
				+ "\nfileMd5 \t" + appMap.get(COUNTRIES[position]).getString("fileMd5")
				+ "\ntitle \t" + appMap.get(COUNTRIES[position]).getString("title")
				+ "\nchangeLog \t" + appMap.get(COUNTRIES[position]).getString("changeLog")
				+ "\ndeveloper \t" + appMap.get(COUNTRIES[position]).getString("developer")
				+ "\ndownloadUrl \t" + appMap.get(COUNTRIES[position]).getString("downloadUrl")
				+ "\niconPath \t" + appMap.get(COUNTRIES[position]).getString("iconPath")
				+ "...";
	    Toast.makeText(this, showInfo, Toast.LENGTH_LONG).show();
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.second, menu);
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

	 private String addAuthParaString(String url, String data) {
 		String result = null;
 		String id = "lbe";
 		String key = "03ff2ad5a1ea48968bfda5c3c18bf2cf";
 		String timeString = "" + System.currentTimeMillis();

 		String token = id + key + data;

 		token = MD5(token);

 		result = url + "?" + "id=" + id + "&timestamp=" + timeString + "&token=" + token;
 		return result;
 	}

		private void getUpdate() throws MalformedURLException, IOException {
			
			
			JSONObject objData = new JSONObject();
			objData.put("model",  android.os.Build.MODEL);
			objData.put("sdkVersion", android.os.Build.VERSION.SDK_INT);
			
			DisplayMetrics dm = new DisplayMetrics();
	        getWindowManager().getDefaultDisplay().getMetrics(dm);
			objData.put("resolution", dm.widthPixels+"x"+dm.heightPixels);
			
			JSONArray userAppArray = new JSONArray();
			JSONArray sysAppArray = new JSONArray();
			
			
		    PackageManager packageManager = this.getPackageManager();  
		    List<PackageInfo> packageInfoList = packageManager.getInstalledPackages(0);  
		    for (int i = 0; i < packageInfoList.size(); i++) {  
		        PackageInfo pak = (PackageInfo) packageInfoList.get(i);  
		        if ((pak.applicationInfo.flags & pak.applicationInfo.FLAG_SYSTEM) <= 0) {
		        	
		        	JSONObject objApp = new JSONObject();
					objApp.put("packageName", pak.applicationInfo.packageName);
					objApp.put("fileMd5", ""); //TODO
					objApp.put("versionCode", pak.versionCode);
					objApp.put("versionName", pak.versionName);
					objApp.put("cerStrMd5", "");//TODO
					
					userAppArray.put(objApp);
		            // customs applications  
		        } else {
		        	// sys apk
		        	JSONObject objApp = new JSONObject();
					objApp.put("packageName", pak.applicationInfo.packageName);
					objApp.put("fileMd5", "");//TODO
					objApp.put("versionCode", pak.versionCode);
					objApp.put("versionName", pak.versionName);
					objApp.put("cerStrMd5", "");//TODO
					
					sysAppArray.put(objApp);
		        }
		    }  
			
	
			JSONObject objApp2 = new JSONObject();
			objApp2.put("packageName", "com.tencent.mm");
			objApp2.put("fileMd5", "b0497c387caa421097add8b0696e4148");
			objApp2.put("versionCode", "192");
			objApp2.put("versionName", "4.2");
			objApp2.put("cerStrMd5", "e52b50104f9c9179ac61f860d4410945");
			
			userAppArray.put(objApp2);
			
//			objData.put("sysApps", sysAppArray);
			objData.put("userApps", userAppArray);

//			System.out.println(objData.toString());
			String dataJsonString = objData.toString();

			/*
			{
			    "model": "C8500S",
			    "sdkVersion": 17,
			    "resolution": "320x240",// �ֻ�ֱ���
			    "sysApps": [],// �ֻ��Դ��ϵͳӦ��
			    "userApps": [ // �û��Լ���װ��Ӧ��
			        {
			            "packageName": "com.tencent.mm"
			            "fileMd5": "b0497c387caa421097add8b0696e4148", // Apk �ļ����ݵ� MD5
						"versionCode": "192", // Apk �ļ��İ汾�ţ�Android ��׼��
						"versionName": "4.2", // Apk �ļ��İ汾�ţ��û��ɼ�
						"cerStrMd5": "e52b50104f9c9179ac61f860d4410945", // Apk ����ǩ��Կ�� MD5
			        },
			        {
			            "packageName": "com.baidu.BaiduMap",
			            "fileMd5": "f80ebdcbda228529c2ab0bd7bcd676b1",// Apk �ļ����ݵ� MD5
			            "versionCode": "431",// Apk �ļ��İ汾�ţ�Android ��׼��
			            "versionName": "5.3.1"// Apk ����ǩ��Կ�� MD5
			        }
			    ]
			}
			*/
			
			
			String urlString = addAuthParaString("http://api.wandoujia.com/v1/update", dataJsonString);
			HttpURLConnection connection = (HttpURLConnection) new URL(urlString).openConnection();

			connection.setDoOutput(true);
			connection.setDoInput(true);
			connection.setRequestMethod("POST");
			connection.setUseCaches(false);

			connection.connect();

			connection.getOutputStream().write(("data=" + dataJsonString).getBytes());

			BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
//			System.out.println("=============================");
//			System.out.println("Contents of post request : " + connection.getResponseCode());
//			System.out.println("=============================");
			StringBuilder lines = new StringBuilder();
			String line;
			while ((line = reader.readLine()) != null) {
				lines.append(line);
			}
			reader.close();

			connection.disconnect();

			JSONObject resJsonObject = new JSONObject(lines.toString());

			JSONArray array = resJsonObject.getJSONArray("userApps");

			System.out.println("new pkg : ");
			for (int i = 0; i < array.length(); i++) {
				JSONObject jObject = (JSONObject) array.get(i);
				appMap.put(jObject.getString("packageName"), jObject);
			}

			JSONArray sysArray = resJsonObject.getJSONArray("sysApps");

			System.out.println("new pkg : ");
			for (int i = 0; i < sysArray.length(); i++) {
				JSONObject jObject = (JSONObject) sysArray.get(i);
				appMap.put(jObject.getString("packageName"), jObject);
			}
			
//			System.out.println("=============================");
//			System.out.println("Contents of post request ends");
//			System.out.println("=============================");
			
		}  
		

		public static String MD5(String plainText) {

			byte[] bytes = null;
			try {
				bytes = plainText.getBytes("UTF-8");
			} catch (UnsupportedEncodingException e) {
			}
			String reString = md5(bytes);

			return reString;

		}

		public synchronized static String md5(byte[] plainByte) {
			try {
				MessageDigest md = MessageDigest.getInstance("MD5");
				md.update(plainByte);
				byte b[] = md.digest();
				int i;
				StringBuffer buf = new StringBuffer("");
				for (int offset = 0; offset < b.length; offset++) {
					i = b[offset];
					if (i < 0)
						i += 256;
					if (i < 16)
						buf.append("0");
					buf.append(Integer.toHexString(i));
				}
				return buf.toString().toLowerCase();

			} catch (Exception e) {
			}
			return null;
		}

}
