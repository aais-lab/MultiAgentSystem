from libs.agent_message import AgentMessage
from libs.edge_knowledge import EdgeBaseKnowldge
from libs.tools import *


class KNOWLEDGE(EdgeBaseKnowldge):
    def __init__(self):
        super().__init__()
        self.creator_info = createDictFromCsv('creator', 'key', 'value')
        
    @EdgeBaseKnowldge.knowledge
    def actInformation(self, msg:AgentMessage):
        match(msg.Type):
            case 'name':
                self.send_to = msg.From
                self.send_req = 'ReturnMessage'
                self.send_conts = f'I am {self.name}'
                self.sendMessage()

            case 'creator':
                name = self.creator_info['name']
                age = self.creator_info['age']
                height = self.creator_info['height']
                university = self.creator_info['university']

                self.send_to = msg.From
                self.send_req = 'ReturnMessage'
                self.send_conts = f'The creator is {name}. {age}-years-old. Height: {height}cm. He is a member of {university}.'
                self.sendMessage()
            
            # おまじない（どのケースにもヒットしなかった時の処理用）
            case _:
                return 'NotFoundType'
