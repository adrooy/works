package com.taobao.bspatch;

public class Main {

	// D:\work\ali\patchapk

	public static void main(String[] args) {

		String oldFile = "D:\\work\\ali\\patchapk\\Google Play80260017.apk";
		String newFile = "D:\\work\\ali\\patchapk\\Google Play80260021.apk";
		String patchFile = "D:\\work\\ali\\patchapk\\diff.patch";

		BSPatch.bspatch(oldFile, newFile, patchFile);

	}
}
