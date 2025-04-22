from ll_kugou_lyric_api.core import KugouApi

if __name__ == "__main__":
   # api =  KugouApi("朵","赵雷")
   # api =  KugouApi("Kids","Two Door Cinema Club")
   # api =  KugouApi("Пятница (星期五)","Дела Поважнее")
   # api =  KugouApi("You Make My Dreams (Come True)","Daryl Hall & John Oates")

   # api =  KugouApi("背影","赵雷",352000)
   # api =  KugouApi("十万嬉皮","万能青年旅店",285000)
   api =  KugouApi("the prom","GLAIVE",131000)
   print(api.get_kugou_lrc()) 
   
   