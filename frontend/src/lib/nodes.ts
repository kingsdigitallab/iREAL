import data from '$data/processed_data_20240804124721.json';
import _ from 'lodash';
import type { Facet, Node, Result, School } from './types';

export async function getResults(): Promise<Result> {
	let nodes = await getAllNodes();

	nodes = nodes.sort((a, b) => a.school.localeCompare(b.school));

	return {
		nodes,
		schoolsNames: getSchoolsNames(nodes),
		schools: getSchools(nodes),
		keywords: getKeywords(nodes),
		organisations: getOrganisations(nodes),
		people: getPeople(nodes),
		places: getPlaces(nodes),
		topics: getTopics(nodes)
	};
}

export async function getAllNodes(): Promise<Node[]> {
	return data as Node[];
}

function getSchoolsNames(nodes: Node[]): string[] {
	return _.uniqBy(nodes, 'school').map((node) => node.school);
}

export async function getSchools(nodes: Node[]): Promise<School[]> {
	return _(nodes)
		.groupBy('school')
		.entries()
		.map(([school, nodes]) => ({
			name: school,
			slug: nodes[0].file.replace('.json', ''),
			keywords: _.orderBy(getKeywords(nodes).map((keyword) => keyword.name)),
			places: _.orderBy(getPlaces(nodes).map((place) => place.name)),
			topics: _.orderBy(getTopics(nodes).map((topic) => topic.name))
		}))
		.value();
}

export function getKeywords(nodes: Node[], minCount: number = 2): Facet[] {
	const schoolsNames = getSchoolsNames(nodes);

	const keywords = _(nodes)
		.map('excerpt_keywords')
		.map((keywords) => keywords.replace(/^1\.s*/, ''))
		.split(',')
		.map((keyword) => keyword.trim())
		.countBy()
		.entries()
		.map(([keyword, count]) => ({ name: keyword, count }))
		.filter((keyword) => !keyword.name.includes('Aboriginal School'))
		.filter((keyword) => !schoolsNames.some((name) => keyword.name.startsWith(name)))
		.filter((keyword) => !schoolsNames.some((name) => name.startsWith(keyword.name)))
		.filter((keyword) => keyword.count >= minCount)
		.orderBy('keyword')
		.value();

	return keywords;
}

export function getOrganisations(
	nodes: Node[],
	minCount: number = 2
): { organisation: string; count: number }[] {
	const organisations = _(nodes)
		.flatMap('organizations')
		.countBy()
		.entries()
		.map(([organisation, count]) => ({ organisation, count }))
		.filter((organisation) => organisation.count >= minCount)
		.value();

	return organisations;
}

export function getPeople(
	nodes: Node[],
	minCount: number = 2
): { person: string; count: number }[] {
	const people = _(nodes)
		.flatMap('persons')
		.countBy()
		.entries()
		.map(([person, count]) => ({ person, count }))
		.filter((person) => person.count >= minCount)
		.value();

	return people;
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

export function getTopics(nodes: Node[], minCount: number = 2): Facet[] {
	const topics = _(nodes)
		.flatMap('topics')
		.countBy()
		.entries()
		.map(([topic, count]) => ({ name: topic, count }))
		.filter((topic) => topic.count >= minCount)
		.orderBy('topic')
		.value();

	return topics;
}

export async function getSchoolNodes(slug: string): Promise<Node[]> {
	const nodes = await getAllNodes();
	return nodes.filter((node) => node.file === `${slug}.json`);
}
