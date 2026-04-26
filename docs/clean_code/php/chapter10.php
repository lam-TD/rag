<?php

namespace Docs\Clean_code\Php;

use Data\UserCreateData;
use Models\User;
use Repositories\UserRepository;

class UserService {
    public function __construct(private UserRepository $repository)
    {
        
    }

    public function create(UserCreateData $userCreateData)
    {
        // validate data
        // create user
        // hash password
        // send welcome email
        // write audit log
        // assign default role
    }

    public function updateProfile(User $user, $data)
    {
        
    }

    public function changePassword(User $user, string $password)
    {
        $this->repository->update()
    }
}