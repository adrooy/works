package com.lbe.data;

import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.List;

import com.gc.android.market.api.LoginException;
import com.gc.android.market.api.MarketSession;
import com.gc.android.market.api.model.Market.GetAssetResponse;
import com.gc.android.market.api.model.Market.GetAssetResponse.InstallAsset;

public class CrawlPlayApk {

	/**
	 * use local dir and file as "db" to record result:
	 *   apkdone: downloaded
	 *   apknotfree: not purchased
	 *   apkfailed: exceptions, etc
	 *   apktemp: temp
	 */
	public static void main(String[] args) throws Exception {
		//CrawlPlayApk.appDownload("com.antabstudio.gridd");
		
		System.out.print("Login...");
		MarketSession session = playLogin();
		System.out.print("success\n");
		
		System.out.print("Clear previous temp...");
		//Files.delete(Paths.get("apktemp", "*.apk"));
		System.out.print("Done\n");
		
		List<String> lines = Files.readAllLines(Paths.get("200.txt"), Charset.forName("UTF-8"));
		for (String pkgname : lines){
			
			if (Files.exists(Paths.get("apkdone", pkgname + ".apk"), LinkOption.NOFOLLOW_LINKS)) {
				System.out.println(pkgname + ": already downloaded");
				continue;
			}
			
			if (Files.exists(Paths.get("apknotfree", pkgname + ".apk"), LinkOption.NOFOLLOW_LINKS)) {
				System.out.println(pkgname + ": not free app");
				continue;
			}
			
			try {
				Thread.sleep(5000);
				switch (appDownload(session, pkgname)) {
				case 0:
					Files.move(Paths.get("apktemp", pkgname + ".apk"),  Paths.get("apkdone", pkgname + ".apk"), StandardCopyOption.REPLACE_EXISTING);
					//System.out.println(pkgname + ": move from temp to done");
					break;
				case 1:
					Files.createFile(Paths.get("apknotfree", pkgname + ".apk"));
					break;
				default:
					Files.createFile(Paths.get("apkfailed", pkgname + ".apk"));
					break;
				}
			} catch (Exception e) {
				e.printStackTrace();
				continue;
			}

		}		
	
	}

	private static String getEmail() {
		return "lbesunzhennan@gmail.com";
	}

	private static String getPassword() {
		return "lbeprivacy";
	}

	private static String getDeviceId() {
		return "30bb76cf4819b5d2";
	}
	
	public static MarketSession playLogin() {
		MarketSession session = null;
		int failedCount = 0;
		while (true) {
			try {
				session = new MarketSession(true);
				session.login(CrawlPlayApk.getEmail(), CrawlPlayApk.getPassword(), CrawlPlayApk.getDeviceId());
			} catch (LoginException le) {
				System.out.println("Login failed! Please check your email or password in Option.");
				failedCount ++;
				if (failedCount == 3)
					throw le;
				else
					continue;
			} catch (Exception ex) {
				ex.printStackTrace();
				System.out.println("Download failed due to: 1. Bad device ID 2. Internet connection 3. You didn't purchase this app");
				failedCount ++;
				if (failedCount == 3)
					throw ex;
				else
					continue;
			}
			break;
		}
		return session;
	}
	

	// return 0: success
	// return 1: not purchased yet
	// return other: fail
	public static int appDownload(MarketSession session, String assetId) {
		try {
			GetAssetResponse gap = session.queryGetAssetRequest(assetId);
			if (gap.getInstallAssetCount() == 0) {
				System.out.println(assetId + ": Not purchased yet. $$$$$$$$$$$$$$$$$$$$$$$$$$");
				return 1;
			}
			InstallAsset ia = gap.getInstallAsset(0);
			String cookieName = ia.getDownloadAuthCookieName();
			String cookieValue = ia.getDownloadAuthCookieValue();
			URL url = new URL(ia.getBlobUrl());
			HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			conn.setRequestProperty("User-Agent", "Android-Market/2 (sapphire PLAT-RC33); gzip");
			conn.setRequestProperty("Cookie", cookieName + "=" + cookieValue);
			if (conn.getResponseCode() == 302) {
				String location = conn.getHeaderField("Location");
				url = new URL(location);
				conn = (HttpURLConnection) url.openConnection();
				conn.setRequestMethod("GET");
				conn.setRequestProperty("User-Agent", "Android-Market/2 (sapphire PLAT-RC33); gzip");
				conn.setRequestProperty("Cookie", cookieName + "="
						+ cookieValue);
			}
			int appLength = conn.getContentLength();
			InputStream inputstream = (InputStream) conn.getInputStream();
			String fileToSave = "apktemp\\" + assetId + ".apk";
			BufferedOutputStream stream = new BufferedOutputStream(new FileOutputStream(fileToSave));
			byte[] buf = new byte[1024];
			int k = 0;
			int readed = 0;
			int percent = 0;
			while ((k = inputstream.read(buf)) > 0) {
				stream.write(buf, 0, k);
				readed += k;
				if ((readed * 100 / appLength) != percent) {
					percent = readed * 100 / appLength;
					System.out.print("\r" + assetId + ": " + Integer.toString(percent) + "%             "+ Integer.toString(readed) + "/" + Integer.toString(appLength) );
				}
			}
			inputstream.close();
			inputstream = null;
			stream.flush();
			stream.close();
			stream = null;
			if (readed == appLength) {
				System.out.println("\r" + assetId + ": Download finished. ^^^^^^^^^^^^^^^^^^^^^^^^^^");				
				return 0;
			} else {
				System.out.println("\r" + assetId + ": Content length mismatch. !!!!!!!!!!!!!!!!!!!!!!!!");
				return 2;
			}
		} catch (LoginException le) {
			System.out.println(assetId + ": LoginException. !!!!!!!!!!!!!!!!!!!!!!!!");
			return 3;
		} catch (Exception ex) {
			ex.printStackTrace();
			System.out.println(assetId + ": Other Exception. !!!!!!!!!!!!!!!!!!!!!!!!");
			return 4;
		}
	}
	
}
