from django import dispatch

before_post_api = dispatch.Signal(providing_args=["requested_data"])
after_post_api = dispatch.Signal(providing_args=["instance", "requested_data"])

before_put_api = dispatch.Signal(providing_args=["instance", "requested_data"])
after_put_api = dispatch.Signal(providing_args=["instance", "requested_data"])

before_patch_api = dispatch.Signal(providing_args=["instance", "requested_data"])
after_patch_api = dispatch.Signal(providing_args=["instance", "requested_data"])
