const { app } = require('@azure/functions');

app.http('submit', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        try {
            const data = await request.json();
            context.log(`Message received from ${data.email}`);

            return {
                status: 200,
                body: JSON.stringify({ success: true, message: 'Message received successfully!' })
            };
        } catch (error) {
            return {
                status: 400,
                body: JSON.stringify({ success: false, error: 'Invalid request data' })
            };
        }
    }
});
