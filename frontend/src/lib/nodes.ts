import data from '$data/processed_data_20240804124721.json';
import _ from 'lodash';
import type { Facet, Node, Result } from './types';

export async function getOverview(): Promise<Result> {
	let nodes = await getAllNodes();

	nodes = nodes.sort((a, b) => a.school.localeCompare(b.school));

	return {
		nodes,
		schoolsNames: getSchoolsNames(nodes),
		keywords: getKeywords(nodes, 2),
		topics: getTopics(nodes, 2),
		organisations: getOrganisations(nodes, 1),
		people: getPeople(nodes, 1),
		places: getPlaces(nodes, 2)
	};
}

export async function getAllNodes(): Promise<Node[]> {
	return data as Node[];
}

function getSchoolsNames(nodes: Node[]): string[] {
	return _.uniqBy(nodes, 'school').map((node) => node.school);
}

export function getKeywords(nodes: Node[], minCount: number = 1): Facet[] {
	const schoolsNames = getSchoolsNames(nodes);

	const keywords = _(nodes)
		.map('excerpt_keywords')
		.map((keywords) => keywords.replace(/^\d+\.s*/, ''))
		.split(',')
		.map((keyword) => keyword.trim())
		.countBy()
		.entries()
		.map(([keyword, count]) => ({ name: keyword, count }))
		.filter((keyword) => !keyword.name.toLowerCase().includes('aboriginal school'))
		.filter(
			(keyword) =>
				!schoolsNames.some((name) => keyword.name.toLowerCase().includes(name.toLowerCase()))
		)
		.filter(
			(keyword) =>
				!schoolsNames.some((name) => name.toLowerCase().includes(keyword.name.toLowerCase()))
		)
		.filter((keyword) => keyword.count >= minCount)
		.orderBy('name')
		.value();

	return keywords;
}

export function getTopics(nodes: Node[], minCount: number = 1): Facet[] {
	const topics = _(nodes)
		.flatMap('topics')
		.countBy()
		.entries()
		.map(([topic, count]) => ({ name: topic, count }))
		.filter((topic) => topic.count >= minCount)
		.orderBy('name')
		.value();

	return topics;
}

export function getOrganisations(nodes: Node[], minCount: number = 2): Facet[] {
	return getEntities('organizations', nodes, minCount);
}

function getEntities(entityName: string, nodes: Node[], minCount: number = 1): Facet[] {
	const entities = _(nodes)
		.flatMap(entityName)
		.filter((entity) => entity)
		.countBy()
		.entries()
		.map(([entity, count]) => ({ name: entity, count }))
		.filter((entity) => entity.count >= minCount)
		.value();

	return entities;
}

export function getPeople(nodes: Node[], minCount: number = 2): Facet[] {
	return getEntities('persons', nodes, minCount);
}

export function getPlaces(nodes: Node[], minCount: number = 1): Facet[] {
	const places = _(nodes)
		.filter((n) => !_.isEmpty(n.geo))
		.flatMap((n) =>
			// @ts-expect-error: No overload matches this call.
			Object.entries(n.geo).map(([place, coords]) => ({
				name: place,
				coords,
				school: n.school
			}))
		)
		.groupBy('name')
		.entries()
		.map(([place, entries]) => ({
			name: place,
			coords: entries[0].coords,
			count: entries.length,
			schools: _.uniq(entries.map((entry) => entry.school))
		}))
		.filter((place) => place.count >= minCount)
		.value();

	return places;
}

export async function getSchools() {
	let nodes = await getAllNodes();
	nodes = nodes.sort((a, b) => a.school.localeCompare(b.school));

	const allKeywords = getKeywords(nodes, 2);
	const allTopics = getTopics(nodes, 2);
	const allDiseases = getDiseases(nodes, 1);
	const allOrganisations = getOrganisations(nodes, 1);
	const allPeople = getPeople(nodes, 1);
	const allPlaces = getPlaces(nodes, 2);

	return _(nodes)
		.groupBy('school')
		.entries()
		.map(([school, nodes]) => ({
			name: school,
			slug: nodes[0].file.replace('.json', ''),
			keywords: _.orderBy(
				getKeywords(nodes, 1).filter((keyword) => allKeywords.some((k) => k.name === keyword.name))
			),
			topics: _.orderBy(
				getTopics(nodes, 1).filter((topic) => allTopics.some((t) => t.name === topic.name))
			),
			diseases: _.orderBy(
				getDiseases(nodes, 1).filter((disease) => allDiseases.some((d) => d.name === disease.name))
			),
			organizations: _.orderBy(
				getOrganisations(nodes, 1).filter((org) =>
					allOrganisations.some((o) => o.name === org.name)
				)
			),
			persons: _.orderBy(
				getPeople(nodes, 1).filter((person) => allPeople.some((p) => p.name === person.name))
			),

			locations: _.orderBy(
				getPlaces(nodes, 1).filter((place) => allPlaces.some((p) => p.name === place.name))
			)
		}))
		.value();
}

function getDiseases(nodes: Node[], minCount: number = 1): Facet[] {
	return getEntities('diseases', nodes, minCount);
}

export async function getSchoolNodes(slug: string): Promise<Node[]> {
	const nodes = await getAllNodes();
	return nodes.filter((node) => node.file === `${slug}.json`);
}
