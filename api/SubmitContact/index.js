module.exports = async function (context, req) {
    const { name, email, message } = req.body || {};

    if (!name || !email || !message) {
        context.res = {
            status: 400,
            body: "Please provide name, email, and message."
        };
        return;
    }

    context.bindings.tableBinding = {
        PartitionKey: "ContactForm",
        RowKey: Date.now().toString(),
        Name: name,
        Email: email,
        Message: message,
        SubmittedAt: new Date().toISOString()
    };

    context.res = {
        status: 200,
        body: { success: true, message: "Message stored successfully!" }
    };
};
