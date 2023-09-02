""" cli module """

import argparse
import logging
import sys
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])


def serve(args):
    """ serve class """

    logger.info("Running server %s", args)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        ssl_keyfile="./key.pem",
        ssl_certfile="./cert.pem",
        reload=True
    )


def main():
    """ main class """

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_server = subparsers.add_parser("serve", help="start the server")
    parser_server.add_argument("--config", help="path to configuration file")
    parser_server.set_defaults(func=serve)

    args = parser.parse_args()
    serve(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Exiting on KeyboardInterrupt")
    except Exception as exc:
        logger.info("Exiting on unknown error %s", exc)
    finally:
        pass
