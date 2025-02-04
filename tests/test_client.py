from datetime import date, timedelta
from uuid import uuid4

from pydantic import ValidationError
from pytest import mark, raises
from rtmilk import Task

def testClientDeleteWithNoDates(client):
	_ = client.Get('')
	taskToAdd = Task(
		title='title 1',
		tags=['tag1', 'tag2'],
		startDate=None,
		dueDate=None,
		complete=False,
		note='note')
	taskAdded = client.Add(taskToAdd)
	client.Delete(taskAdded)

def testClient(client):
	existingTasks = client.Get('')
	title = f'title: {uuid4()}'
	startDate = date.today()
	dueDate = startDate + timedelta(days=2)
	taskToAdd = Task(
		title=title,
		tags=['tag1', 'tag2'],
		startDate=startDate,
		dueDate=dueDate,
		complete=False,
		note='note')

	client.Add(taskToAdd)
	with raises(ValidationError):
		client.Add(None)
	tasks = client.Get('')
	assert len(tasks) == 1 + len(existingTasks), tasks
	for task in existingTasks:
		for index in range(len(tasks)): # pylint: disable=consider-using-enumerate
			if task.title == tasks[index].title:
				del tasks[index]
				break
	assert len(tasks) == 1, tasks
	assert tasks[0].title == title
	assert sorted(tasks[0].tags) == ['tag1', 'tag2']
	assert tasks[0].startDate == startDate
	assert tasks[0].dueDate == dueDate
	assert tasks[0].complete is False

	noTasks = client.Get('', lastSync=tasks[0].modifiedTime + timedelta(seconds=1))
	assert len(noTasks) == 0

	client.Delete(tasks[0])

@mark.asyncio
async def testClientAsync(client):
	existingTasks = await client.GetAsync('')
	title = f'title: {uuid4()}'
	startDate = date.today()
	dueDate = startDate + timedelta(days=2)
	taskToAdd = Task(
		title=title,
		tags=['tag1', 'tag2'],
		startDate=startDate,
		dueDate=dueDate,
		complete=False,
		note='note')

	await client.AddAsync(taskToAdd)
	with raises(ValidationError):
		await client.AddAsync(None)
	tasks = await client.GetAsync('')
	assert len(tasks) == 1 + len(existingTasks), tasks
	for task in existingTasks:
		for index in range(len(tasks)): # pylint: disable=consider-using-enumerate
			if task.title == tasks[index].title:
				del tasks[index]
				break
	assert len(tasks) == 1, tasks
	assert tasks[0].title == title
	assert sorted(tasks[0].tags) == ['tag1', 'tag2']
	assert tasks[0].startDate == startDate
	assert tasks[0].dueDate == dueDate
	assert tasks[0].complete is False

	noTasks = await client.GetAsync('', lastSync=tasks[0].modifiedTime + timedelta(seconds=1))
	assert len(noTasks) == 0

	await client.DeleteAsync(tasks[0])
