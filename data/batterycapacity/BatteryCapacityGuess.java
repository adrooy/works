package com.lbe.security.service.battery.util;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipFile;

import net.ricecode.similarity.JaroWinklerStrategy;
import net.ricecode.similarity.SimilarityScore;
import net.ricecode.similarity.StringSimilarityService;
import net.ricecode.similarity.StringSimilarityServiceImpl;

public class BatteryCapacityGuess {

	private class RealData {
		public RealData (String vendor_in, String model_in, String original_model_in) {
			vendor = vendor_in;
			model = model_in;
			original_model = original_model_in;
		}
		public String vendor;
		public String model;
		public String original_model;
	}
	
	private class BatteryData {
		public BatteryData (String fullname_in, String model_in, String val_in) {
			fullname = fullname_in;
			model = model_in;
			val = val_in;
		}
		public String fullname;
		public String model;
		public String val;
	}
	
	private class ResultData {
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
	
	private ArrayList<ResultData> mResult;
	private ArrayList<BatteryData> mBatteryData;
	private ArrayList<RealData> mRealData;
	private StringSimilarityService mSSS;
	int mVendorNotMatch;
	int mSSSNotMatch;
	int mSSSNull;
	
	
	public BatteryCapacityGuess() {
		mResult = new ArrayList<ResultData>();
		mBatteryData = new ArrayList<BatteryData>();
		mRealData = new ArrayList<RealData>();
		mSSS = new StringSimilarityServiceImpl(new JaroWinklerStrategy());
		mVendorNotMatch = 0;
		mSSSNotMatch = 0;
		mSSSNull = 0;
	}
	
	private void genMatchResult() {
		try {
			
			for (RealData real : mRealData) {
				
				ArrayList<BatteryData> candidateList = new ArrayList<BatteryData>();

				for (BatteryData battery : mBatteryData) {
					if (battery.fullname.contains(real.vendor)) {
						candidateList.add(battery);
						//System.out.println ("Realdata: " + real.getElement0() +","+ real.getElement1() + ".  Vendor match:" + real.getElement1() + ". Add model candidate: " + model_number);
					}
				}
				
				if (candidateList.size() == 0) {
					mVendorNotMatch ++;
					System.out.println(real.vendor);
					candidateList = mBatteryData;
					continue;
				}
				
				ArrayList<String> forSSS = new ArrayList<String>();
				for (BatteryData battery : candidateList) {
					//System.out.println ("genMatchResult: add candidate model in SSS: " + battery.model);
					forSSS.add(battery.model);
				}
				SimilarityScore nearestModel = mSSS.findTop(forSSS, real.model); // model match
				if (nearestModel != null) {
					boolean added = false;
					//System.out.println ("genMatchResult: nearestModel in SSS: " + nearestModel.getKey());
					for (BatteryData battery : candidateList) {
						if (battery.model.equals(nearestModel.getKey())) {
							mResult.add(new ResultData(real, battery.fullname, battery.val, nearestModel.getScore()));
							added = true;
							break;
						}
					}
					if (!added)
						mSSSNotMatch++;
				} else
					mSSSNull++;
			}
			
		} catch (Exception e) {
			e.printStackTrace();			
		}
	}
	
	private boolean init(String realDataFile, String batteryDataFile) {
		
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";
		String model, vendor;
	 
		
		Pattern pattern1 = Pattern.compile(
				"([a-zA-Z-][a-zA-Z-][0-9]+)|" +					// aa999
				"([a-zA-Z-][0-9]+[a-zA-Z-][a-zA-Z-])|" +		// a999bb
				"([a-zA-Z-][a-zA-Z-][0-9]+[a-zA-Z-])|" +		// aa999b
				"([0-9]+[a-zA-Z-][a-zA-Z-])|" +					// 999bb
				"([a-zA-Z-][0-9]+[a-zA-Z-])|" +					// a999b
				"([a-zA-Z-][0-9]+)|" +							// a999
				"([0-9]+[a-zA-Z-])|" +							// 999b
				"([0-9]+)");									// 999
		
		try {
	 
			br = new BufferedReader(new FileReader(realDataFile));
			while ((line = br.readLine()) != null) {
				String[] values = line.toLowerCase().split(cvsSplitBy);
				if (values.length < 2)
					continue;
				vendor = values[0];
				model = values[1];
				Matcher matcher = pattern1.matcher(model);
				String model_number = model;
				if (matcher.find())
					model_number = matcher.group(0);
				mRealData.add(new RealData(vendor, model_number, model));
				//System.out.println ("real: " + vendor + ", " + model);
			}
			br.close();
			br = null;

			
			br = new BufferedReader(new FileReader(batteryDataFile));
			while ((line = br.readLine()) != null) {
				String[] values = line.toLowerCase().split(cvsSplitBy);
				if (values.length < 3)
					continue;
				Matcher matcher = pattern1.matcher(values[1]);
				String model_number = values[1];
				if (matcher.find())
					model_number = matcher.group(0);
				BatteryData	n = new BatteryData(values[1], model_number, values[2]);
				mBatteryData.add(n);
			}
			br.close();
			br = null;
			return true;
	 
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		
		return false;
	}
	
	private void dumpMatchResult(String resultFile) {
		try {
			PrintWriter writer = new PrintWriter(resultFile, "GBK");
			for (ResultData r : mResult) {
				writer.println(String.format("%s-%s,\t\t%s,\t\t\t\t\t%s,\t\t%f", r.real.vendor, r.real.original_model, r.matched_string, r.matched_value, r.score));
			}
			writer.close();			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public static int getBatteryCapacity(String vendor, String model, int default_value) {
		try {
			int ret = default_value;
			ZipFile zf  = new ZipFile("batterycapacity.ini");
			
			zf.close();
			return ret;
		} catch (IOException e) {
			return default_value;
		}
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {

		BatteryCapacityGuess self = new BatteryCapacityGuess();
		
		if (!self.init("D:\\workspace\\data\\batterycapacity\\offical_names_distinct.csv", "D:\\workspace\\data\\batterycapacity\\battery_newer.csv")) {
			System.out.println("Init data fail. exit");
			return ;
		}
		
		self.genMatchResult();
		
		self.dumpMatchResult("D:\\workspace\\data\\batterycapacity\\match_result.csv");
		
		System.out.println(String.format("Missed: %d+%d+%d=%d. Total: %d\n", self.mVendorNotMatch, self.mSSSNotMatch, self.mSSSNull, self.mVendorNotMatch + self.mSSSNotMatch + self.mSSSNull, self.mRealData.size()));

	}

}
