
from WebsocketTest.common.utils import *
from urllib.parse import quote_plus 
from WebsocketTest.common import WSBaseApi
from WebsocketTest.common.WSBaseApi import WSBaseApi

class ApiTestRunner(WSBaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.answer_text = ""
    def build_params(self):
        """准备请求参数"""  
        return {
            "header": {
                "appid": self.appId,
                "scene": self.scene,
                "sid": self.sid or generate_random_string(), # 奥迪sid为空时，不会自生成
                "uid": self.uid,
                "usrid": ""
            },
            "parameter": {
                "custom": {
                    "custom_data": {
                        "SessionParams": {
                            "isLog": "true",
                            "app_id": "",
                            "attachparams": {
                                "iat_params": {
                                    "compress": "raw",
                                    "da": "0",
                                    "domain": "aiui-automotiveknife",
                                    "dwa": "wpgs",
                                    "encoding": "utf8",
                                    "eos": "600",
                                    "format": "json",
                                    "isFar": "0",
                                    "opt": "2",
                                    "ufsa": "1",
                                    "vgap": "200",
                                    "accent": self.accent,
                                    "language": self.language
                                },
                                "nlp_params": {
                                    "llmEnv": "test",
                                    "ovs_cluster":"AUDI",
                                    "city": "合肥",
                                    "compress": "raw",
                                    "encoding": "utf8",
                                    "format": "json",
                                    "devid": "",
                                    "news": {
                                        "pageNo": 1,
                                        "pageSize": 20
                                    },
                                    "flight": {
                                        "pageNo": 1,
                                        "pageSize": 20
                                    },
                                    "ovs_version": {
                                        "weather": "3.5"
                                    },
                                    "user_defined_params": {},
                                    "weather_airquality": "true",
                                    "mapU": {
                                        "pageNo": 1,
                                        "pageSize": 20
                                    },
                                    "deviceId": self.deviceId,
                                    "userId": self.userId,
                                    "asp_did": self.asp_did,
                                    "vWtoken": self.token,
                                    "car_identity": self.car_identity,
                                    "theme": "standard",
                                    "vin": self.vin,
                                    "interactive_mode": "fullDuplex",
                                    "did": self.did,
                                    "smarthome": {
                                        "jd": {
                                            "newSession": "true",
                                            "sessionId": "123456789",
                                            "userId": "9adbd42d-618f-4752-ad6d-9cb382079e25"
                                        }
                                    },
                                    "train": {
                                        "pageNo": 1,
                                        "pageSize": 20
                                    }
                                },
                                "tts_params": {
                                    "bit_depth": "16",
                                    "channels": "1",
                                    "encoding": "speex-wb",
                                    "frame_size": "0",
                                    "sample_rate": "16000"
                                }
                            },
                            "aue": "speex-wb",
                            "bit_depth": "16",
                            "channels": "1",
                            "city_pd": "",
                            "client_ip": "112.132.223.243",
                            "dtype": "text",
                            "frame_size": "0",
                            "msc.lat": "31.837463",
                            "msc.lng": "117.17",
                            "pers_param": self.pers_param,
                            "sample_rate": "16000",
                            "scene": self.scene,
                            "stmid": "0",
                            "uid": self.uid,
                            "debug": self.debug,
                            "debugx": self.debugx,
                            "category": self.category
                        },
                        "UserParams": encode_base64(self.UserParams),
                        "UserData": quote_plus(self.UserData)
                    }
                }
            },
            "payload": {
                "text": {
                    "compress": "raw",
                    "encoding": "utf8",
                    "format": "plain",
                    "plainText": self.plainText,
                    "status": 3
                }
            }
        }
    async def handle_v1_chain(self, ws):
        """
        处理5.0链路逻辑：
        - 根据接收到的消息执行不同的操作
        - 当'action'为'started'时，读取文件并发送数据块
        - 发送结束标识
        - 当'action'为'result'且'sub'为'stream_tpp'时，返回内容
        """
        while True:
            _msg = await ws.recv()
            # print(_msg)
            try:
                msg = json.loads(_msg)
                code = safe_get(msg, ["header","code"])
                if code != 0:
                    logger.error(f'请求错误: {code}, {msg}')
                    break
                else:
                    answer = safe_get(msg, ["payload","results","text","intent","answer"])
                    answerText = safe_get(answer, ["text"])
                    if answerText:
                        self.answer_text += answerText
                    if msg['header']['status']=="2" or msg['header']['status']=="3":  # 返回结果接收完成
                        if self.answer_text:
                            answer["text"] = self.answer_text     
                        self.response = msg
                        return
                        
            except Exception as e:
                logger.error(f"error in handle_v1_chain :{e}")
                break
 
    
