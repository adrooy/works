package com.lbe.security.service.battery.util;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipInputStream;

import net.ricecode.similarity.JaroWinklerStrategy;
import net.ricecode.similarity.SimilarityScore;
import net.ricecode.similarity.StringSimilarityService;
import net.ricecode.similarity.StringSimilarityServiceImpl;

public class BatteryCapacityGuess {

	private static class RealData {
		public RealData (String vendor_in, String model_in, String original_model_in) {
			vendor = vendor_in;
			model = model_in;
			original_model = original_model_in;
		}
		public String vendor;
		public String model;
		public String original_model;
	}
	
	private static class BatteryData {
		public BatteryData (String fullname_in, String model_in, String val_in) {
			fullname = fullname_in;
			model = model_in;
			val = val_in;
		}
		public String fullname;
		public String model;
		public String val;
	}
	
	private static class ResultData {
		public ResultData(RealData real_in, String matched_string_in, String matched_value_in, double score_in) {
			real = real_in;
			matched_string = matched_string_in;
			matched_value = matched_value_in;
			score = score_in;
		}
		public RealData real;
		public String matched_string;
		public String matched_value;
		public double score;
		
	}
	
	private static Pattern modelRegEx; 
	static {
		modelRegEx = Pattern.compile(
			"([a-zA-Z-][a-zA-Z-][0-9]+)|" +					// aa999
			"([a-zA-Z-][0-9]+[a-zA-Z-][a-zA-Z-])|" +		// a999bb
			"([a-zA-Z-][a-zA-Z-][0-9]+[a-zA-Z-])|" +		// aa999b
			"([0-9]+[a-zA-Z-][a-zA-Z-])|" +					// 999bb
			"([a-zA-Z-][0-9]+[a-zA-Z-])|" +					// a999b
			"([a-zA-Z-][0-9]+)|" +							// a999
			"([0-9]+[a-zA-Z-])|" +							// 999b
			"([0-9]+)");									// 999	
	}
	
	private static String findLongestMatcherGroup(Pattern regex, String src) {
		Matcher matcher = modelRegEx.matcher(src);
		String result = "";
		while (matcher.find()) {
			String s = matcher.group();
			if (s.length() >= result.length())
				result = s;
		}
		return result;	// return "" if not found
	}
	
	private static String findFirstMatcherGroup(Pattern regex, String src) {
		Matcher matcher = modelRegEx.matcher(src);
		String result = "";
		if (matcher.find()) {
				result = matcher.group(0);
		}
		return result;	// return "" if not found
	}	
			
	private static RealData prepareRealData (String vendor, String original_model) {
		String model = findLongestMatcherGroup(modelRegEx, original_model);
		if (model.length() == 0)
			model = original_model;
		return new RealData(vendor, model, original_model);		
	}
	
	private static ArrayList<BatteryData> prepareBatteryData (String batteryDataFile) {
		ArrayList<BatteryData> batteryList = new ArrayList<BatteryData>();
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";
		try {
			// we packed the "batterycapacity.ini" into a zip named "batterycapacity.ini"
			
			// Android version:
			// ZipInputStream zis = new ZipInputStream(LBEApplication.getApplication().getAssets().open("batterycapacity.ini"));
			//zin.getNextEntry();
			//br = new BufferedReader(new InputStreamReader(zin));
			
			// PC zip version:
			//ZipInputStream zin = new ZipInputStream(new FileInputStream(batteryDataFile));
			//zin.getNextEntry();
			//br = new BufferedReader(new InputStreamReader(zin));

			// PC txt version:
			br = new BufferedReader (new InputStreamReader(new FileInputStream(batteryDataFile)));
			
			while ((line = br.readLine()) != null) {
				String[] values = line.toLowerCase().split(cvsSplitBy);
				// line format: SAMSUNG I9500 GALAXY S4, 2600
				if (values.length < 2)
					continue;
				
				String model = findLongestMatcherGroup(modelRegEx, values[0]);
				if (model.length() == 0)
					model = values[0];
				batteryList.add(new BatteryData(values[0], model, values[1]));
			}
			br.close();
			//zin.close();
 		} catch (Exception e) {
 			//e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					//e.printStackTrace();
				}
			}
		}		
		return batteryList;
	}

	private static ResultData getMatchResult(RealData real, ArrayList<BatteryData> batteryList) {
		try {
			ArrayList<BatteryData> candidateList = new ArrayList<BatteryData>();
			for (BatteryData battery : batteryList) {
				if (battery.fullname.contains(real.vendor))
					candidateList.add(battery);
			}

			if (candidateList.size() == 0)
				candidateList = batteryList;

			ArrayList<String> forSSS = new ArrayList<String>();
			for (BatteryData battery : candidateList)
				forSSS.add(battery.model);

			StringSimilarityService sss = new StringSimilarityServiceImpl(new JaroWinklerStrategy());
			SimilarityScore nearestModel = sss.findTop(forSSS, real.model);

			if (nearestModel != null) {
				for (BatteryData battery : candidateList) {
					if (battery.model.equals(nearestModel.getKey())) {
						return new ResultData(real, battery.fullname, battery.val, nearestModel.getScore());
					}
				}
			}
		} catch (Exception e) {
		}
		return null;
	}
	

	public static int getBatteryCapacity(String vendor, String model, int default_value) {
		// MTK手机软件方案商开发开发时因主板芯片通用一般都用alps作为manufacturer
		// 所以得去取model的第一个字母单词作为vendor
		if (vendor.equalsIgnoreCase("alps")) {
			String[] strs = model.split("[^A-Za-z]",2);
			if (strs.length == 2)
				vendor = strs[0];
			else
				vendor = "";	// 找不到的话，去匹配所有型号
		}
		RealData real = prepareRealData (vendor.toLowerCase(), model.toLowerCase());
		ArrayList<BatteryData> batteryList = prepareBatteryData ("batterycapacity.ini.txt");
		ResultData result = getMatchResult(real, batteryList);
		if (result != null)
			return Integer.parseInt(result.matched_value);
		else
			return default_value;
	}
		
}
