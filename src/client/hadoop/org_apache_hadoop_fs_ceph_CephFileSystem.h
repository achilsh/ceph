/* DO NOT EDIT THIS FILE - it is machine generated */
#include <jni.h>
/* Header for class org_apache_hadoop_fs_ceph_CephFileSystem */

#ifndef _Included_org_apache_hadoop_fs_ceph_CephFileSystem
#define _Included_org_apache_hadoop_fs_ceph_CephFileSystem
#ifdef __cplusplus
extern "C" {
#endif
#undef org_apache_hadoop_fs_ceph_CephFileSystem_DEFAULT_BLOCK_SIZE
#define org_apache_hadoop_fs_ceph_CephFileSystem_DEFAULT_BLOCK_SIZE 8388608LL
/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_initializeClient
 * Signature: ()J
 */
JNIEXPORT jlong JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1initializeClient
  (JNIEnv *, jobject);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_copyFromLocalFile
 * Signature: (JLjava/lang/String;Ljava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1copyFromLocalFile
  (JNIEnv *, jobject, jlong, jstring, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_copyToLocalFile
 * Signature: (JLjava/lang/String;Ljava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1copyToLocalFile
  (JNIEnv *, jobject, jlong, jstring, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_getcwd
 * Signature: (J)Ljava/lang/String;
 */
JNIEXPORT jstring JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1getcwd
  (JNIEnv *, jobject, jlong);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_setcwd
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1setcwd
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_rmdir
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1rmdir
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_mkdir
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1mkdir
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_unlink
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1unlink
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_rename
 * Signature: (JLjava/lang/String;Ljava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1rename
  (JNIEnv *, jobject, jlong, jstring, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_exists
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1exists
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_getblocksize
 * Signature: (JLjava/lang/String;)J
 */
JNIEXPORT jlong JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1getblocksize
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_getfilesize
 * Signature: (JLjava/lang/String;)J
 */
JNIEXPORT jlong JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1getfilesize
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_isdirectory
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1isdirectory
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_isfile
 * Signature: (JLjava/lang/String;)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1isfile
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_getdir
 * Signature: (JLjava/lang/String;)[Ljava/lang/String;
 */
JNIEXPORT jobjectArray JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1getdir
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_mkdirs
 * Signature: (JLjava/lang/String;I)I
 */
JNIEXPORT jint JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1mkdirs
  (JNIEnv *, jobject, jlong, jstring, jint);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_open_for_append
 * Signature: (JLjava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1open_1for_1append
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_open_for_read
 * Signature: (JLjava/lang/String;)I
 */
JNIEXPORT jint JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1open_1for_1read
  (JNIEnv *, jobject, jlong, jstring);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_open_for_overwrite
 * Signature: (JLjava/lang/String;I)I
 */
JNIEXPORT jint JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1open_1for_1overwrite
  (JNIEnv *, jobject, jlong, jstring, jint);

/*
 * Class:     org_apache_hadoop_fs_ceph_CephFileSystem
 * Method:    ceph_kill_client
 * Signature: (J)Z
 */
JNIEXPORT jboolean JNICALL Java_org_apache_hadoop_fs_ceph_CephFileSystem_ceph_1kill_1client
  (JNIEnv *, jobject, jlong);

#ifdef __cplusplus
}
#endif
#endif
