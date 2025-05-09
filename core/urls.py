"""
* Zibal Payment Test Task
*
* Developer: Ali Sharifi
* Email: alisharifyofficial@gmail.com
* Website: ali-sharify.ir
* GitHub: github.com/alisharify7/zibal
* Repository: https://github.com/alisharify7/zibal
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("transactions/", include("transactions.urls")),
]
