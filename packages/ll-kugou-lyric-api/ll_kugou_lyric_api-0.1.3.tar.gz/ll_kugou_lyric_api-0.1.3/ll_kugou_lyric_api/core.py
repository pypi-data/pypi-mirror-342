import base64
import requests
import re

class KugouApi:
    SEARCH_URL = 'http://krcs.kugou.com/search'
    DOWNLOAD_URL = 'https://lyrics.kugou.com/download'

    def __init__(self, title, artist, duration=None): 
        self.title = title
        self.artist = artist
        self.duration = duration

    def get_kugou_lrc(self):
        """
        获取酷狗歌词，如果未命中尝试去除括号后重试。
        """
        for attempt in range(2):
            keyword = self._build_keyword()
            duration = self.duration
            res = self._search_lrc(keyword,duration)
            if not res:
                return None

            candidates = res.get("candidates", [])
            if candidates:
                result = self._select_best_candidate(candidates)
                if result is not None:
                    id, accesskey = result
                    return self._download_best_lrc(id,accesskey)
            
            if attempt == 0:
                print("未命中歌词，尝试清理括号内容后重试...")
                self._clean_metadata()
            else:
                print(f'接口{self.SEARCH_URL}返回未找到candidates[]错误!入参:{keyword},{duration}')

        return None

    def _build_keyword(self):
        return f"{self.artist} - {self.title}"

    def _search_lrc(self, keyword, duration):
        params = {
            'ver': '1',
            'man': 'yes',
            'client': 'mobi',
            'keyword': keyword,  # 👈 关键点！
            'duration': duration or '',
            'hash': '',
            'album_audio_id': ''
        }
        try:
            response = requests.get(self.SEARCH_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                # with open("./search.json", "w", encoding="utf-8") as file:
                #     json.dump(data, file, indent=4, ensure_ascii=False)
                return data
        except Exception as e:
            print(f"请求出错: {e}")
        return None

    def _select_best_candidate(self, candidates):
        """
        从候选项中选出最优的 candidate，返回其 id 和 accesskey
        :param candidates: 搜索结果中的 candidates 列表
        :return: (id, accesskey) 或 None
        """
        try:
            best = min(
                candidates,
                key=lambda c: (
                    abs(c['duration'] // 1000 - self.duration // 1000) if self.duration else -c['score'],
                    -c['score']
                )
            )
            # print(f'歌曲id:{best["id"]},歌曲时长:{best["duration"]},歌曲评分:{best["score"]}')
            return best["id"], best["accesskey"]
        except (KeyError, ValueError, IndexError) as e:
            print(f"[候选选择错误] {e}")
            return None

    def _download_best_lrc(self, id,accesskey):
        try:
            params = {
                'ver': '1',
                'client': 'pc',
                'id': id,
                'accesskey': accesskey,
                'fmt': 'lrc',
                'charset': 'utf8'
            }
            res = requests.get(self.DOWNLOAD_URL, params=params).json()
            return base64.b64decode(res['content']).decode("utf-8")
        except Exception as e:
            print(f"解析歌词出错: {e}")
            return None

    def _clean_metadata(self):
        self.title = self._remove_brackets(self.title)
        self.artist = self._remove_brackets(self.artist)

    @staticmethod
    def _remove_brackets(text):
        return re.sub(r'[\(\（\[\【\〔\{｛][^\)\）\]\】\〕\}｝]*[\)\）\]\】\〕\}｝]', '', text)
