package com.taobao.bspatch;

import android.os.Environment;


/**
 * Created by lianbing.klb on 13-10-31.
 */
public class BSPatch {
    static {
        try {//防止出现不支持的CPU，如MIPS等，而导致出现Error
			System.loadLibrary("BSPatch");
        } catch (Throwable e) {
        	System.out.println(e);
        }
    }

	public static void test() {
		String a = Environment.getExternalStorageDirectory().getAbsolutePath() + "/LBE_Security_CI_5.4.8027.apk";
		String b = Environment.getExternalStorageDirectory().getAbsolutePath() + "/36.apk";
		String c = Environment.getExternalStorageDirectory().getAbsolutePath() + "/27-36.bs";
		System.out.println(a);
		int res = bspatch(a, b, c);
		
		a = Environment.getExternalStorageDirectory().getAbsolutePath() + "/LBE_Security_CI_5.4.8027.apk";
		 b = Environment.getExternalStorageDirectory().getAbsolutePath() + "/43.apk";
		 c = Environment.getExternalStorageDirectory().getAbsolutePath() + "/27-43.bs";
		System.out.println(a);
		 res = bspatch(a, b, c);
		
		System.out.println("res:" + res);
	}

    /**
     * bsdiff算法合并
     *
     * @param old_file   基础文件路径
     * @param new_file   新生成文件路
     * @param patch_file 补丁文件路径
     * @return 1表示成功
     */
    public static native int bspatch(String old_file, String new_file, String patch_file);
}
