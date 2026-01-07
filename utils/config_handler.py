# 配置文件处理器
import yaml

from utils.path_tool import get_abs_path


# 加载rag配置文件
def load_rag_config(config_path: str = get_abs_path("config/rag.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 加载chroma配置文件
def load_chroma_config(config_path: str = get_abs_path("config/chroma.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
# 加载prompt配置文件
def load_prompt_config(config_path: str = get_abs_path("config/prompt.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
# 加载agent配置文件
def load_agent_config(config_path: str = get_abs_path("config/agent.yaml"), encoding: str = "utf-8"):
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


# 得到对应的配置项
rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompt_config()
agent_conf = load_agent_config()