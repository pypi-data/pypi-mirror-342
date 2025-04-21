# Copyright (c) 2019-2025 Watsen Networks. All Rights Reserved.

_A=None
import sys,signal,asyncio,functools
from datetime import datetime,timedelta,UTC
from yangcore.periodic import forever_loop
from.dal import DataAccessLayer,AuthenticationFailed,NodeNotFound
from.rcsvr import RestconfServer
from.native import NativeViewHandler
from.import utils
class ContractNotAccepted(Exception):0
class UnrecognizedAcceptValue(Exception):0
class UnrecognizedModeValue(Exception):0
class BadCommandLineParams(Exception):0
LOOP=_A
SIG=_A
NVH=_A
def signal_handler(name):global SIG;SIG=name;LOOP.stop()
def init(firsttime_cb_func,db_url,cacert_param=_A,cert_param=_A,key_param=_A,app_name=_A):
	F=db_url;E=app_name;D=key_param;C=cert_param;B=cacert_param;assert E is not _A
	if B is not _A and F.startswith('sqlite:'):raise BadCommandLineParams('The "sqlite" dialect does not support the "cacert" parameter.')
	if(C or D)and not B:raise BadCommandLineParams('The "cacert" parameter must be specified whenever the '+'"key" and "cert" parameters are specified.')
	if(C is _A)!=(D is _A):raise BadCommandLineParams('The "key" and "cert" parameters must be specified together.')
	H=False
	try:G=DataAccessLayer(F,B,C,D,_A,_A,_A,E)
	except(SyntaxError,AssertionError,AuthenticationFailed)as A:raise A
	except NotImplementedError:H=True
	if H is True:
		try:I=firsttime_cb_func()
		except ContractNotAccepted:sys.exit(0)
		except Exception as A:raise A
		try:assert E is not _A;G=DataAccessLayer(F,B,C,D,I,_A,_A,E)
		except Exception as A:raise A
	assert G is not _A;return G
def run(dal,endpoint_settings):
	a='periodic_callback';Z='somehow_change_callback';Y='subtree_change_callback';X='change_callback';W='delete_callback';V='create_callback';U='yangcore:native-interface';T='SIGHUP';J='yangcore:use-for';H=endpoint_settings;G='schema_path';E=dal;D='callback_func';global LOOP;global SIG;global NVH;LOOP=asyncio.new_event_loop();LOOP.add_signal_handler(signal.SIGHUP,functools.partial(signal_handler,name=T));LOOP.add_signal_handler(signal.SIGTERM,functools.partial(signal_handler,name='SIGTERM'));LOOP.add_signal_handler(signal.SIGINT,functools.partial(signal_handler,name='SIGINT'));LOOP.add_signal_handler(signal.SIGQUIT,functools.partial(signal_handler,name='SIGQUIT'))
	while SIG is _A:
		I=[];C=E.handle_get_config_request('/ietf-restconf-server:restconf-server',{});K=LOOP.run_until_complete(C)
		for B in K['ietf-restconf-server:restconf-server']['listen']['endpoints']['endpoint']:
			if B[J]=='native-interface'or B[J]==U:
				NVH=NativeViewHandler(E,LOOP);A=H[U]
				if V in A:
					for N in A[V]:NVH.register_create_callback(N[G],N[D])
				if W in A:
					for O in A[W]:NVH.register_delete_callback(O[G],O[D])
				if X in A:
					for P in A[X]:NVH.register_change_callback(P[G],P[D])
				if Y in A:
					for Q in A[Y]:NVH.register_subtree_change_callback(Q[G],Q[D])
				if Z in A:
					for R in A[Z]:NVH.register_somehow_change_callback(R[G],R[D])
				if a in A:
					for L in A[a]:NVH.register_periodic_callback(L['period'],L['anchor'],L[D])
				S=RestconfServer(LOOP,E,B,NVH)
			else:
				M=B[J]
				if M not in H:raise KeyError('Error: support for the configured endpoint "use-for" '+'interface "'+M+'" was not supplied in the '+'"endpoint_settings" parameter in the yangcore.run() method.')
				b=H[M]['view-handler'];c=b(E,H[B[J]]['yang-library-func'](),NVH);S=RestconfServer(LOOP,E,B,c)
			I.append(S);del B;B=_A
		del K;K=_A;d=LOOP.create_task(forever_loop(NVH));LOOP.run_forever();d.cancel()
		for F in I:C=F.app.shutdown();LOOP.run_until_complete(C);C=F.runner.cleanup();LOOP.run_until_complete(C);C=F.app.cleanup();LOOP.run_until_complete(C);del F;F=_A
		del I;I=_A
		if SIG==T:SIG=_A
	LOOP.close()