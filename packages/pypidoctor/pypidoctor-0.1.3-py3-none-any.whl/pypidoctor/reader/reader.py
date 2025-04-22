from llama_index.core.readers.base import BaseReader
from typing import List, Dict,Optional
from llama_index.core import Document
import yaml

def get_data_from_md(text):
    _,infos,content = text.split("---",2)
    data = yaml.safe_load(infos)
    return data, content
    
class CustObsidianReader(BaseReader):
    def load_data(self, file_path: str,
                        extra_info: Optional[Dict] = None) -> List[Document]:
        # 自定义读取逻辑
        with open(file_path, 'r') as file:
            text = file.read()
        data,content = get_data_from_md(text)
        # 使用状态
        status = data.get('编辑状态',None)
        topic = data.get('topic','')
        describe = data.get('describe','')
        creation_date = data.get("creation date",'')
        tags = data.get('tags', [])
        link = data.get('链接','')
        content_cut = content[:6000]
        if len(content_cut) != len(content):
            print(topic,'is too long ***')


        document = Document(text=f"topic: {topic} content: {content}", 
                            metadata={"topic":topic,
                                      "status":status,
                                      "creation_date":str(creation_date),
                                      "tags":tags,
                                      "link":link},
                           )
        return [document]


