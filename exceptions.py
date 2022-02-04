import traceback

def handle(msg, stacktrace=False):
        if stacktrace:
            print(f'\n-    (×_×) -      [STACK]      -\n')
            traceback.print_exc()
            print('\n')

        print('\n-    (×_×) -      [SADGE]      -\n')
        print(msg)
        exit(0)
