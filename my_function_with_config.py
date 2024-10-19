import os

# @nuclio.configure
#
# function.yaml:
#   apiVersion: "nuclio.io/v1"
#   kind: NuclioFunction
#   metadata:
#     name: my-new-function  # Changed the function name here
#     namespace: nuclio
#   spec:
#     env:
#     - name: MY_ENV_VALUE
#       value: my value
#     handler: my_function_with_config:my_entry_point
#     runtime: python:3.8-alpine  # Specify the Python runtime version
#     triggers:
#       http:
#         kind: http
#         attributes:
#           serviceType: NodePort
#       periodic:
#         attributes:
#           interval: 3s
#         class: ""
#         kind: cron

def my_entry_point(context, event):
    # use the logger, outputting the event body
    context.logger.info_with('Got invoked',
        trigger_kind=event.trigger.kind,
        event_body=event.body,
        some_env=os.environ.get('MY_ENV_VALUE'))

    # check if the event came from cron
    if event.trigger.kind == 'cron':
        # log something
        context.logger.info('Invoked from cron')
    else:
        # return a response
        return 'A string response'
