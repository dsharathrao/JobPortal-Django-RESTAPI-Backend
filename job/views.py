from django.db.models import Avg, Count, Max, Min
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .filters import JobsFilter
from .models import Job
from .serializers import JobSerializer


@api_view(['GET'])
def getAllJobs(request):
    
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by("id"))

    resPerPage = 3

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = JobSerializer(queryset, many=True)
    if len(serializer.data) == 0:
        return Response({"message": "Not Found"},status=status.HTTP_404_NOT_FOUND)
    
    return Response({"resPerPage": resPerPage, "jobs": serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getJob(request,pk):
    job = get_object_or_404(Job, id=pk)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def newJob(request):
    data = request.data
    job = Job.objects.create(**data)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateJob(request,pk):
    job = get_object_or_404(Job, id=pk)

    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']

    job.save()

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    job.delete()

    return Response({'message': 'Job is Deleted.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTopicStats(request, topic):
    args = {'title__icontains':topic}
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({"message": "Not stats found for {topic}".format(topic=topic)}, status=status.HTTP_404_NOT_FOUND)
    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_positions = Avg('positions'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary'),
    )
    return Response(stats, status=status.HTTP_200_OK)
