package com.lbe.security.service.battery.util;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import net.ricecode.similarity.JaroWinklerStrategy;
import net.ricecode.similarity.SimilarityScore;
import net.ricecode.similarity.StringSimilarityService;
import net.ricecode.similarity.StringSimilarityServiceImpl;


public class BatteryCapacityGuessOld {

	private static class RealData {
		public RealData (String vendor_in, String model_in, String original_model_in) {
			vendor = vendor_in;
			model = model_in;
		}
		public String vendor;
		public String model;
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
			matched_value = matched_value_in;
		}
		public String matched_value;
		
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
	
	private static RealData prepareRealData (String vendor, String original_model) {
		Matcher matcher = modelRegEx.matcher(original_model);
		String model = original_model;
		if (matcher.find())
			model = matcher.group(0);
		return new RealData(vendor, model, original_model);		
	}
	
	private static final String Battery_Name = "batterycapacity.ini";
	private static ArrayList<BatteryData> prepareBatteryData () {
		ArrayList<BatteryData> batteryList = new ArrayList<BatteryData>();
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";
		try {
			ZipInputStream zin = new ZipInputStream(new FileInputStream(Battery_Name));
			zin.getNextEntry();
			br = new BufferedReader(new InputStreamReader(zin));
			while ((line = br.readLine()) != null) {
				String[] values = line.toLowerCase().split(cvsSplitBy);
				// line format: SAMSUNG I9500 GALAXY S4, 2600
				if (values.length < 2)
					continue;
				Matcher matcher = modelRegEx.matcher(values[0]);
				String model = values[0];
				if (matcher.find())
					model = matcher.group(0);
				batteryList.add(new BatteryData(values[0], model, values[1]));
			}
			br.close();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (Exception e) {
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
		try {
			RealData real = prepareRealData (vendor.toLowerCase(), model.toLowerCase());
			ArrayList<BatteryData> batteryList = prepareBatteryData ();
			ResultData result = getMatchResult(real, batteryList);
			return Integer.parseInt(result.matched_value);
		} catch (Exception e) {
		}
		return default_value;
	}
		
}