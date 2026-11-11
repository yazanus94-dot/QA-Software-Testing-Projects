export const PASSWORD = 'secret_sauce';

export const users = {
  standard: { username: 'standard_user', password: PASSWORD },
  locked: { username: 'locked_out_user', password: PASSWORD },
  problem: { username: 'problem_user', password: PASSWORD },
  glitch: { username: 'performance_glitch_user', password: PASSWORD },
} as const;

export const checkoutInfo = { firstName: 'Yazan', lastName: 'Tester', postalCode: '00000' };
