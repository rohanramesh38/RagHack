from promptflow import tool
from typing import List

@tool
def should_generate_reply(queries: List[str], chunks: List) -> dict:

  reference = ''
  for chunk in chunks:
    if('filepath' in chunk):
      reference+="\n"+chunk["filepath"]

  
  return {'reference':reference,'success':True}
  #return True if chunks or not queries else False