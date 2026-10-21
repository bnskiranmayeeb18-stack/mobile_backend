const { v4: uuidv4 } = require('uuid');

function correlationIdMiddleware(req, res, next) {
  const correlationId = req.headers['x-correlation-id'] || uuidv4();
  req.correlationId = correlationId;
  res.setHeader('X-Correlation-ID', correlationId);
  
  // Structured log
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level: 'info',
    correlationId: correlationId,
    method: req.method,
    path: req.originalUrl
  }));
  
  next();
}

module.exports = correlationIdMiddleware;
