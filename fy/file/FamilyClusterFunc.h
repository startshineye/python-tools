#pragma once
#include "stdio.h"
#include "stdlib.h"
#include "float.h"  
#include <string.h>
#include <malloc.h>
#include "math.h"
#include <time.h>

extern "C"
{
	struct Sys_Parameters
{
	float windowLen[15];  //���ڳ���
	float freqBins[15];   //Ƶ������
	float csThd[15];      //һ��������
	float corrThd[15];    //�������
	float sigma_A[15];    //��λ�Ƿ�������
	float sigma_V[15];    //���ٷ�������
	float sigma_F;        //Ƶ�ʷ�������
	float sigma_T;        //ʱ�䷽�� �ٷֱ� ͨ��Ϊ100%�����벽��һ�� 10��
	float timeThd;        //ʱ����ֵ���� ͨ��Ϊ200%    Ĭ��Ϊ20��
	int   nFamilyMax;     //family ������Ԫ����
	int   nFamilyMin;     //family �����ٵ�Ԫ����
	float ThresholdDistance;
	// ��������
	float VelocityMax;    //�������ֵ��ֵ
	float VelocityMin;    //������Сֵ��ֵ

	float freqHighLim;
	float freqLowLim;
	float overlapRate;

};

void ArrayFamilyForm(float (*OutputAV)[15], float (*matrixA)[15],float (*matrixV)[15],
	float(*matrixC)[15],int nLineNumTime,int nColumnNumFreq,float nTimeStep,float Fs,Sys_Parameters structParameter);
}