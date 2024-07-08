import path from 'path';

import Hapi from '@hapi/hapi';
import inert from '@hapi/inert';

const port = process.env.PORT || 3000;

const FILES = /\.(js|js.map|woff|woff2|svg|bmp|jpg|jpeg|gif|png|ico|css)(\?v=\d+\.\d+\.\d+)?$/;

const init = async () => {
  const server = Hapi.server({
    port,
    host: '0.0.0.0',
  });

  await server.register(inert);

  server.route({
    method: 'GET',
    path: '/{path*}',
    handler: (request, h) => {
      console.log(`Request received for: ${request.path}`);

      const matched = FILES.test(request.path);
      console.log(`Does request match FILES regex? ${matched}`);

      const filePath = matched
        ? path.join(process.cwd(), 'dist', request.path)
        : path.join(process.cwd(), 'dist', 'index.html');
      console.log(`Returning file: ${filePath}`);

      if (FILES.test(request.path)) {
        return h.file(path.join(process.cwd(), request.path));
      }

      return h.file(path.join(process.cwd(), 'index.html'));
    },
  });

  await server.start();
  console.log('Server running on %s', server.info.uri);
};

process.on('unhandledRejection', (err) => {
  console.log(err);
  process.exit(1);
});

init();
