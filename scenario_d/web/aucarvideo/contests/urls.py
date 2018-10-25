# -- encoding: utf-8 --

from django.urls import path
from django.conf.urls import url

from contests.views import ContestCreate
# from contests.views import ContestList
# from contests.views import ContestUpdate
# from contests.views import ContestDetail
# from contests.views import ContestAdminList
# from contests.views import ContestDelete

# from contests.views import VideoCreate
# from contests.views import VideoAdminList
# from contests.views import VideoProcessingStatus


urlpatterns = [
    path('contest/add/', ContestCreate.as_view(), name='contest_create'),
    # path('contest/<int:pk>/delete/',ContestDelete.as_view(),name='contest_delete'),
    # path('contest/<str:url>/update/',ContestUpdate.as_view(),name='contest_update'),
    # path('contest/<str:url>/detail/',ContestDetail.as_view(),name='contest_detail'),
    # path('contest/list/',ContestList.as_view(),name='contest_list'),
    # path('admin/contest/list/',ContestAdminList.as_view(),name='contest_admin_list'),

    # path('contest/<int:pk>/video/add/',VideoCreate.as_view(),name='video_create'),
    # path('contest/<int:pk>/video/list/',VideoAdminList.as_view(),name='video_admin_list'),
    # path('api/contest/videos/status/',VideoProcessingStatus.as_view(),name='video_status'),
    # path('contest/<int:url>/video/list/',VideoAdminList.as_view(),name='video_admin_list'),


]

