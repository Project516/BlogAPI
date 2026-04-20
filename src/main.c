#include "mongoose.h"
#include <time.h>

static void ev_handler(struct mg_connection *c, int ev, void *ev_data)
{
    if (ev == MG_EV_HTTP_MSG)
    {
        struct mg_http_message *hm = (struct mg_http_message *) ev_data;

        if (mg_match(hm->uri, mg_str("/api/hello"), NULL))
        {
            mg_http_reply(c, 200, "", "{%m:%d}\n", MG_ESC("status"), 1);

        } 
        else 
        {
            struct mg_http_serve_opts opts =
            {
                .root_dir = ".",
                .fs = &mg_fs_posix
            };
            mg_http_serve_dir(c, hm, &opts);
        }
    }
}

int main (void)
{
    struct mg_mgr mgr;
    mg_mgr_init(&mgr);

    mg_http_listen(&mgr, "http://0.0.0.0:8000", ev_handler, NULL);

    while (1)
    {
        mg_mgr_poll(&mgr, 1000);
    }

    return 0;
}