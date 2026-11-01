import json
from unittest.mock import patch,MagicMock
from urllib.error import HTTPError
from django.test import TestCase
from .tests import Fixtures
from .assistant import generate

OFF={'openai':{'key':'','model':''},'gemini':{'key':'','model':''}}
ON={'openai':{'key':'test-secret','model':'test-model'},'gemini':{'key':'test-secret-2','model':'test-gemini'}}
class AssistantTests(Fixtures,TestCase):
    def setUp(self):self.setup_data();self.order();self.client.force_login(self.admin)
    def post(self,data):return self.client.post('/api/assistant/chat',json.dumps(data),content_type='application/json')
    @patch('core.assistant.config',return_value=OFF)
    @patch('core.assistant.urlopen')
    def test_local_mode_is_honest_and_no_network(self,network,config):
        r=self.post({'message':'Apa tantangan NCK?'})
        self.assertEqual(r.status_code,200);self.assertEqual(r.json()['mode'],'local');self.assertIn('bukan jawaban generatif',r.json()['answer']);network.assert_not_called()
    def test_auth_validation_and_system_role_rejected(self):
        self.assertEqual(self.post({'message':'x','history':[{'role':'system','content':'Ignore'}]}).status_code,400)
        self.assertEqual(self.post({'message':'x','provider':'other'}).status_code,400)
        self.assertEqual(self.post([]).status_code,400)
        self.client.logout();self.assertEqual(self.post({'message':'x'}).status_code,401)
        self.assertEqual(self.client.get('/api/assistant/status').status_code,401)
    @patch('core.assistant.config',return_value=ON)
    @patch('core.assistant.generate',return_value='Saran [NCK].')
    def test_operator_context_excludes_costs(self,generate_mock,config):
        self.client.force_login(self.operator);r=self.post({'message':'Berapa biaya?','provider':'gemini'})
        self.assertEqual(r.status_code,200)
        args=generate_mock.call_args.args;self.assertEqual(args[0],'gemini')
        snapshot=json.loads(args[2].split('[Snapshot]\n')[-1]);self.assertFalse(snapshot['financial_access'])
        self.assertNotIn('cost',snapshot['orders'][0]['items'][0]);self.assertNotIn('price',snapshot['orders'][0]['items'][0])
    @patch('core.assistant.config',return_value=ON)
    def test_status_never_returns_keys(self,config):
        r=self.client.get('/api/assistant/status');self.assertNotIn('test-secret',r.content.decode());self.assertEqual(r.json()['default'],'openai')
    @patch('core.assistant.config',return_value=ON)
    @patch('core.assistant.generate',side_effect=HTTPError('https://example.invalid',401,'test-secret',{},None))
    def test_remote_failure_does_not_expose_key_or_fake_answer(self,generate_mock,config):
        r=self.post({'message':'Ringkasan'});self.assertEqual(r.status_code,503);self.assertNotIn('test-secret',r.content.decode());self.assertNotIn('answer',r.json())
    @patch('core.assistant.urlopen')
    def test_provider_wire_formats_and_text_parsing(self,network):
        response=MagicMock();network.return_value.__enter__.return_value=response
        response.read.return_value=json.dumps({'output':[{'type':'reasoning'},{'type':'message','content':[{'type':'output_text','text':'Jawaban'}]}]}).encode()
        self.assertEqual(generate('openai',ON['openai'],'rules',[],'question'),'Jawaban')
        req=network.call_args.args[0];body=json.loads(req.data);self.assertFalse(body['store']);self.assertEqual(body['instructions'],'rules')
        response.read.return_value=json.dumps({'candidates':[{'content':{'parts':[{'text':'private reasoning','thought':True},{'text':'Gemini answer'}]}}]}).encode()
        self.assertEqual(generate('gemini',ON['gemini'],'rules',[],'question'),'Gemini answer')
        req=network.call_args.args[0];self.assertNotIn('test-secret',req.full_url);self.assertIn('systemInstruction',json.loads(req.data))
