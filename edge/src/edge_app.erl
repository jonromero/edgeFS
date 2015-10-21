%%%-------------------------------------------------------------------
%% @doc edge public API
%% @end
%%%-------------------------------------------------------------------

-module('edge_app').

-behaviour(application).

-export([start/2]).
-export([stop/1]).

start(_Type, _Args) ->
    %% When the node starts, contact one Edge to get other nodes
    connect_to_edgefs(EdgeNode),

	Dispatch = cowboy_router:compile([
		{'_', [
			{"/", api_handler, []}
		]}
	]),
	{ok, _} = cowboy:start_http(http, 100, [{port, 8080}], [
		{env, [{dispatch, Dispatch}]}
	]),
	edge_sup:start_link().

stop(_State) ->
	ok.

