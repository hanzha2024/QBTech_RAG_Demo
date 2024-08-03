# -*- coding: utf-8 -*-
from zhipuai import ZhipuAI

# refer to https://open.bigmodel.cn/dev/api#sdk_auth
def get_ans(prompt):
    client = ZhipuAI(api_key="c099b530fbc7650e5a8a148af27348e9.w10hPQllGWNdNZ1b")  # please use your own api key

    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        top_p=0.3,
        temperature=0.45,
        max_tokens=1024,
        stream=True,
    )
    ans = ""
    for trunk in response:
        ans += trunk.choices[0].delta.content
    return ans


def get_respone(prompt):
    client = ZhipuAI(api_key="c099b530fbc7650e5a8a148af27348e9.w10hPQllGWNdNZ1b")

    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        top_p=0.3,
        temperature=0.45,
        max_tokens=1024,
        stream=True,
    )
    return response