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
    

            
    
