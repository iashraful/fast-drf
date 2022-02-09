from django import dispatch

before_post_api = dispatch.Signal()
after_post_api = dispatch.Signal()

before_put_api = dispatch.Signal()
after_put_api = dispatch.Signal()

before_patch_api = dispatch.Signal()
after_patch_api = dispatch.Signal()
