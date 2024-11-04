import { getQuestions } from '$lib/nodes';
import type { PageServerLoad } from './$types';

export const load = (async () => {
	const questions = await getQuestions();

	return {
		questions
	};
}) satisfies PageServerLoad;
