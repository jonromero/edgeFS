-module(api_handler).

-export([init/2]).

init(Req, Opts) ->
	Req2 = cowboy_req:reply(200, [
		{<<"content-type">>, <<"text/plain">>}
	], <<"Hello world!">>, Req),
	{ok, Req2, Opts}.


search_for_file(Filename) ->
    case search_local(Filename) of
        {found, Fragments} ->
            get_fragments(Fragments);
        {not_found} ->
            edge:sync(Fragments),
            edge:search(Filename)
    end.


store_file(Filename) ->
    Encrypted_data = encrypt(Filename),
    Fragments = break_in_pieces(Encrypted_data),
    Nodes = edge:availability(),
    upload_to_edge(Nodes, Fragments).
    

is_available() ->
    yes.


%% whenever there is an edge command, it should be followed by a score


edge:search(Filename) ->    
    Results = map(search, Edges),
    score(Results),
    get_file(Results, Filename).
    
       
%% -1 point for non responsive
%% to be updated     
score(Edges) ->
    ok.
    
